from urllib import quote
from flask import Blueprint, jsonify, abort, request
from stringer_api import phantom, cache, dynamo, app
from ..dao import matches as matches_dao

tournaments_api = Blueprint('tournaments_api', __name__)


@tournaments_api.route('/tournaments')
def live_tournaments():
    matches = matches_dao.get()
    tournament_names = set(map(lambda x: x['tournament'], matches))
    tournaments = [build_tournament(tournament_name, matches) for tournament_name in tournament_names]

    return jsonify(tournaments=tournaments)


def build_tournament(tournament_name, matches):
    return {
        'name': tournament_name,
        'matches': filter(lambda x: x['tournament'] == tournament_name, matches),
        'tournament_url': build_tournament_url(tournament_name)
    }


def build_tournament_url(tournament_name):
    return request.url_root + 'tournaments/' + quote(tournament_name)


@tournaments_api.route('/tournaments/<name>')
def live_tournament(name):
    matches = matches_dao.get()
    matches_for_tournament = filter(lambda x: x['tournament'] == name, matches)
    tournaments = [{ 'name': name,  'matches': matches_for_tournament }]

    tournament = {
        'name': name,
        'matches': matches_for_tournament
    }

    return jsonify(tournaments=tournaments)
