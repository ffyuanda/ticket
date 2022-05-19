from flask import Flask
from flask import request
from loguru import logger
from flask_cors import CORS
from models import retrieve_email, get_dates_by_email
from models import register as _register

app = Flask(__name__)
CORS(app)

logger.add("ticket.log", format="{time} {file} {level} {message}",\
            level="DEBUG", rotation="1 week", backtrace=True, diagnose=True)

@app.route("/retrieve", methods=['POST'])
def retrieve():
    try:
        email = request.json['email']
    except KeyError:
        logger.error(f"bad request email key")
    logger.info(f"retrieving email: {email}")
    retrieve_email(email)
    return {'result': 'OK'}, 200

@app.route("/register", methods=['POST'])
def register():
    try:
        email = request.json['email']
        date = request.json['date']
    except KeyError:
        pass
    logger.info(f"registering email: {email} with date: {date}")
    _register(date, email)
    return {'result': 'OK'}, 200


@app.route("/dates", methods=['POST'])
def get_dates():
    try:
        email = request.json['email']
    except KeyError:
        pass
    logger.info(f"getting dates by email: {email}")
    dates = get_dates_by_email(email)
    return {'result': 'OK', 'dates': dates}, 200
