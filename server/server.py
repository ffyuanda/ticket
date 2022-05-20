from flask import Flask
from flask import request
from loguru import logger
from flask_cors import CORS
from models import retrieve_email, get_dates_by_email, delete_date_from_email
from models import register as _register


# initialize the logger, thanks loguru! <3
logger.add("server.log", format="{time} {file} {level} {message}",\
               level="DEBUG", rotation="1 week", backtrace=True, diagnose=True)

app = Flask(__name__)
CORS(app)


@logger.catch
@app.route("/retrieve", methods=['POST'])
def retrieve():
    email = request.json['email']

    logger.info(f"retrieving email: {email}")
    retrieve_email(email)
    return {'result': 'OK'}, 200


@logger.catch
@app.route("/register", methods=['POST'])
def register():
    email = request.json['email']
    date = request.json['date']

    logger.info(f"registering email: {email} with date: {date}")
    _register(date, email)
    return {'result': 'OK'}, 200


@logger.catch
@app.route("/dates", methods=['POST'])
def get_dates():
    email = request.json['email']

    logger.info(f"getting dates by email: {email}")
    dates = get_dates_by_email(email)
    return {'result': 'OK', 'dates': dates}, 200


@logger.catch
@app.route("/del-date", methods=['DELETE'])
def del_date():
    email = request.json['email']
    date = request.json['date']
    
    logger.info(f"deleting date: {date} from email: {email}")
    delete_date_from_email(email, date)
    return {'result': 'OK'}, 200
