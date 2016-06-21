from flask import Blueprint, jsonify
from betfair import constants
import json
from stringer_api import client

account_api = Blueprint('account_api', __name__)


@account_api.route("/account")
def get_account():
    account_funds_resp = client.get_account_funds()
    account = {
        'balance': account_funds_resp['available_to_bet_balance'],
        'exposure': account_funds_resp['exposure'],
        'tennisProfit': get_tennis_profit(),
        'wallet': account_funds_resp['wallet']
    }

    return jsonify(account)


def get_tennis_profit():
    items = get_items()
    tennis_items = filter(is_tennis_item, items)
    profit = reduce(lambda cumulative, item: cumulative + item.amount, tennis_items, 0.0)

    return profit


def get_items(from_record=0):
    all_items = []
    get_more_items = True

    while get_more_items:
        account_statement = client.get_account_statement(from_record=from_record)
        all_items.extend(account_statement.account_statement)
        get_more_items = account_statement.more_available
        from_record = from_record + len(account_statement.account_statement)

    return all_items


def is_tennis_item(item):
    item_data = json.loads(item.item_class_data['unknownStatementItem'])

    if 'eventTypeId' in item_data and item_data['eventTypeId'] is 2:
        return True

    return False
