from crypt import methods
from flask import Flask
from flask import request
from loguru import logger
from flask_cors import CORS
from models import retrieve_email

app = Flask(__name__)
CORS(app)

@app.route("/retrieve", methods=['POST'])
def retrieve():
    try:
        email = request.json['email']
    except KeyError:
        print(request.form)
        logger.error(f"bad request email key")
    logger.info(f"retrieving email: {email}")
    retrieve_email(email)
    return {'result': 'OK'}, 200
