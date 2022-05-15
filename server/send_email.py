from email.message import EmailMessage
from email.utils import formataddr
from models import get_emails_by_date
from aiosmtplib import SMTPRecipientsRefused
from loguru import logger
import aiosmtplib
import asyncio

port = 587  # For SSL
smtp_server = "smtp-mail.outlook.com"
sender_email = "ffyuanda@outlook.com"  # Enter your address
password = input("Type your password and press enter (for email sending): ")

async def send_email(email: str, ticket):
    message = EmailMessage()
    message["From"] = formataddr(('HKA Ticket Tracker', sender_email))
    message["To"] = email
    message["Subject"] = "Ticket Update"
    message.set_content(str(ticket))
    try:
        await aiosmtplib.send(message, hostname=smtp_server, port=port, username=sender_email,\
                            password=password, start_tls=True)
        logger.success(f"email sent: To: {email} Ticket: \n{str(ticket)}")
    except SMTPRecipientsRefused as e:
        logger.warning(f"recipient refused: {str(e)}")

async def send_emails(tickets: list):
    aws = []
    for ticket in tickets:
        emails = get_emails_by_date(ticket.date)

        for email in emails:
            task = asyncio.create_task(send_email(email, ticket))
            aws.append(task)
    
    await asyncio.gather(*aws)
