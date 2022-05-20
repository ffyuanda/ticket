from variables import cookies, headers, url, template_payload
from models import get_dates_from_database, get_emails_by_date
from send_email import send_emails
from loguru import logger
from time import sleep
import json
import copy
import grequests
import requests
import asyncio


# initialize the logger, thanks loguru! <3
logger.add("ticket.log", format="{time} {file} {level} {message}",\
               level="DEBUG", rotation="1 week", backtrace=True, diagnose=True)


class Ticket:

    def __init__(self, date, time, num, type) -> None:
        self.date = date
        self.time = time
        self.num = num
        self.type = type
        self.renewed = False

    def __eq__(self, other):
        if self.date == other.date and \
           self.time == other.time and \
           self.type == other.type:
            return True
        return False

    def __repr__(self) -> str:
        return f"<{type(self).__name__}> (date={self.date}, time={self.time}, \
num={self.num}, type={self.type}, renewed={self.renewed})"

    def __str__(self) -> str:
        return f"Ticket Date: {self.date}\nTicket Time: {self.time}\n\
Ticket Type: {self.type}\nTicket Remaining Number: {self.num}"

    def renew(self):
        self.renewed = True

    def expire(self):
        self.renewed = False


def make_payload_from_date(date: str) -> dict:
    """
    Make an actual payload from a date, using the template payload.
    """
    payload = copy.copy(template_payload)
    payload["toDate"] = date
    payload = json.dumps(payload)
    return {'siteResJson': payload}


def get_AsyncRequest(date: str) -> grequests.AsyncRequest:
    """
    Prepare a POST AsyncRequest that represents the Response of tickets from a date.
    """
    data = make_payload_from_date(date)
    req = grequests.post(url, cookies=cookies, headers=headers, data=data)
    return req


@logger.catch
def get_tickets_responses(dates: list) -> list:
    """
    Concurrently retrieve a list of Response from dates.
    """
    responses = [get_AsyncRequest(date) for date in dates]
    responses = grequests.map(responses)
    return responses


@logger.catch
def parse_tickets_response(response: requests.Response) -> list:
    """
    Parse the response into a list of available (num > 0) Ticket objects.
    """
    ticket_list = []
    response_json = response.json()
    for mes in response_json["message"]:
        for seat in mes['seatList']:
            if int(seat['num']) > 0:
                ticket = Ticket(mes['startDate'], mes['goTime'], seat['num'], seat['seatTypeName'])
                ticket_list.append(ticket)

    return ticket_list
 

def update_alive_tickets(alive_tickets: list, ticket: Ticket) -> bool:
    """
    Update the alive_tickets list:
    if the ticket is matched with an alive_ticket from alive_tickets,
    renew the alive_ticket; else append the ticket to alive_tickets.

    If ticket is not new, i.e. this ticket was in active_tickets,
    return False; otherwise, return True.
    """
    for alive_ticket in alive_tickets:
        if ticket == alive_ticket:
            alive_ticket.renew()
            return False

    ticket.renew()
    alive_tickets.append(ticket)
    return True


def expire_all_tickets(alive_tickets: list):
    """
    Expire all tickets in alive_tickets.
    """

    for alive_ticket in alive_tickets:
        alive_ticket.expire()


def remove_expired_tickets(alive_tickets: list):
    """
    Remove all expired tickets from active_tickets.

    This is mainly used to remove the tickets that are expired (which means in
    a new round of request fetching, these tickets become unavailable). Once
    they are removed, when next time they are available again, we will know that
    the emails should be sent regarding this ticket.
    """
    i = 0
    while i < len(alive_tickets):
        if not alive_tickets[i].renewed:
            alive_tickets.pop(i)
        else:
            i += 1


def main():

    logger.info("Program start.")

    # Keep a list of tickets that are currently available.
    # When a new ticket is available, it should be added to this
    # list; and a ticket should be removed from this list only
    # when its num (remaining number) goes to 0. This list also
    # helps to determine if we should send an email to the users:
    # if we are adding a ticket to this list (which means this
    # ticket just got available, from 0 to positive), send email to
    # them.
    alive_tickets = []

    # Ever running loop to retrieve and analyze data.
    while True:
        logger.debug("main loop start")

        send_email_tickets = []
        expire_all_tickets(alive_tickets)
        logger.debug("all tickets set to expired")

        dates = get_dates_from_database()
        logger.info(f"dates to query: {str(dates)}")

        responses = get_tickets_responses(dates)
        logger.info(f"responses retrieved: {str(responses)}")

        for response in responses:

            # Get a list of available tickets.
            tickets = parse_tickets_response(response)
            
            for ticket in tickets:
                logger.info(f"ticket: \n{str(ticket)}")

                should_send_email = update_alive_tickets(alive_tickets, ticket)
                if should_send_email:
                    send_email_tickets.append(ticket)
                    logger.debug(f"append to send_email_tickets: {str(ticket)}")
        
        remove_expired_tickets(alive_tickets)
        logger.debug("removed all expired tickets from alive_tickets")

        logger.debug("async send_emails start")
        logger.info(f"send_email_tickets: \n{str(send_email_tickets)}")

        asyncio.run(send_emails(send_email_tickets))

        logger.debug("async send_emails end")

        logger.debug("sleeping for 10 seconds...")
        sleep(10)

        logger.debug("main loop end")


if __name__ == '__main__':

    main()
