import boto3
import logging
from flask import Flask
from flask_cache import Cache
from flask_cors import CORS
from betfair import Betfair
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

app = application = Flask(__name__)
app.config.from_envvar('STRINGER_API_CONFIG')

client = Betfair(app.config['BETFAIR_APPLICATION_KEY'], app.config['BETFAIR_PEM_PATH'])
client.login(app.config['BETFAIR_USER_NAME'], app.config['BETFAIR_PASSWORD'])

cache = Cache(config=app.config['CACHE_CONFIG'])
cache.init_app(app)

CORS(app, origins=app.config['CORS'])

dynamo = boto3.client('dynamodb', region_name='eu-west-1')

phantom = None
try:
    phantom = webdriver.PhantomJS(app.config['PHANTOM_PATH'])
except WebDriverException as e:
    app.logger.error(e)
except Exception as e:
    app.logger.error(e)

from stringer_api.matches import matches_api
from stringer_api.account import account_api
from stringer_api.players import players_api
app.register_blueprint(matches_api)
app.register_blueprint(account_api)
app.register_blueprint(players_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
