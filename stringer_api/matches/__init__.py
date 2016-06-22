from flask import Blueprint, jsonify, request
from ..dao import matches as matches_dao

matches_api = Blueprint('matches_api', __name__)


@matches_api.route('/matches')
def matches():
    matches = matches_dao.get()
    filtered_matches = _filter(matches)

    result = {
        'matches': filtered_matches,
        'meta': {
            'matchCount': len(matches),
            'filteredMatchCount': len(filtered_matches)
        }
    }

    return jsonify(result)


def _filter(matches):
    mens = request.args.get('mens')
    if mens:
        mens = req_bool_conversion(mens)
        matches = filter(lambda m: m['mens'] == mens, matches)

    singles = request.args.get('singles')
    if singles:
        singles = req_bool_conversion(singles)
        matches = filter(lambda m: m['singles'] == singles, matches)

    return matches


def req_bool_conversion(string):
    if string == "true":
        return True
    return False
