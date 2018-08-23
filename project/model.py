import requests
from project import logger

# API address
address = 'http://127.0.0.1:5000/api/'


def call_buy_beverage(user_id, beverage_id):
    request = address + 'beverage_club/' + user_id + '-' + beverage_id

    response = None
    try:
        response = requests.post(request)
        logger.logger_rest("Buy Beverage - Scanner", response, response.url)
    except Exception:
        logger.logger_error(user_id, beverage_id)

    if response is None:
        return 0
    else:
        return response.status_code


def get_user(user_id):
    request = address + 'user/' + user_id

    response = None
    try:
        response = requests.get(request)
        logger.logger_rest("Get User Name - Scanner", response, response.url)
    except ConnectionError:
        logger.logger_error(user_id, user_id)
    except Exception:
        print("fail")


    if response is None:
        return 0
    else:
        return response.json().get('name')


def get_beverage_name(beverage_id):
    request = address + 'beverage_club/' + beverage_id

    response = None
    try:
        response = requests.get(request)
        logger.logger_rest("Get Beverage Name - Scanner", response, response.url)
    except ConnectionError:
        logger.logger_error(beverage_id, beverage_id)
    except Exception:
        print("The right exception was not caught...")

    if response is None:
        return 0
    else:
        return response.json().get('name')
