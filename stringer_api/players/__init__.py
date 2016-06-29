from flask import Blueprint, jsonify, abort, request
from bs4 import BeautifulSoup
from urllib import quote
import json
from stringer_api import phantom, cache, dynamo, app

players_api = Blueprint('players_api', __name__)


@players_api.route('/players/<betfair_name>')
def player(betfair_name):
    result = get_player(betfair_name)

    return jsonify(player=result)


def get_player(betfair_name):
    tennis_abstract_name = get_tennis_abstract_name(betfair_name)
    career_page = BeautifulSoup(get_career_page(tennis_abstract_name), 'html.parser')
    biography = career_page.find('p', {'id': 'biog'})
    tds = biography.find_all('td')

    result = {
        "id": betfair_name,
        "name": get_player_name(biography),
        "dateOfBirth": get_player_dob(tds)
    }

    return result


def get_tennis_abstract_name(betfair_name):
    name_mapping = dynamo.get_item(TableName='PlayerNameMapping', Key={'BetfairName': {'S': str(quote(betfair_name))}})
    if 'Item' not in name_mapping:
        abort(404)

    return name_mapping['Item']['TennisAbstractName']['S']


@cache.cached(timeout=21600, key_prefix='rawTennisAbstract%s')
def get_career_page(tennisAbstractName):
    app.logger.info("Request made to: {0}".format("http://www.tennisabstract.com/cgi-bin/player.cgi?p=" + tennisAbstractName + '&f=ACareerqq'))
    phantom.get("http://www.tennisabstract.com/cgi-bin/player.cgi?p=" + tennisAbstractName + '&f=ACareerqq')

    return phantom.page_source


def get_player_name(raw_page):
    content = raw_page.find('b').text

    return content


def get_player_dob(biog_tds):
    raw_dob = str(biog_tds[2].text.strip())

    return raw_dob[15:]


def get_from_cache(name):
    return cache.get(quote(name))


def store_in_cache(key, val):
    cache.set(key, val)
