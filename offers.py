#!/usr/bin/env python3

import time
import datetime

import bot
import queries

from binance.exceptions import BinanceAPIException

def cancel_current_best_bid(best_offer_price_, best_bid_price_):
    print(f'\n| @@@{datetime.datetime.now().strftime("%H:%M")}@@@')
    print(f'| OFFER at price {best_offer_price_} was EXECUTED;')

    try:
        bot.CLIENT.cancel_order(symbol=bot.TRADING_PAIR, orderId=queries.get_order_id(best_bid_price_))  # CANCEL currentlly 'BEST BID'
        print(f'| Cancelling BEST BID: {best_bid_price_}')
    except BinanceAPIException:
        print('[!!!] Error while canceling BEST BID')

# A function for replacing the executed OFFER
def update_rel_to_best_offer(best_offer_price_, best_bid_price_):
    if not queries.order_active(best_offer_price_):  # If the NEW best OFFER order is not already or yet present on the market
        print(f'| Placing NEW BEST OFFER at higher price: {best_offer_price_}')
        bot.CLIENT.order_limit_sell(symbol=bot.TRADING_PAIR, quantity=bot.COINS_PER_ORDER, price=best_offer_price_)  # Replacing executed OFFER with NEW best OFFER
        time.sleep(1)
        
    if not queries.order_active(best_bid_price_):  # If the NEW best BID order is not already or yet present on the market
        print(f'| Placing NEW BEST BID at higher price: {best_bid_price_}')
        bot.CLIENT.order_limit_buy(symbol=bot.TRADING_PAIR, quantity=bot.COINS_PER_ORDER, price=best_bid_price_)  # Placing a BID (NEW best BID) at a WINDOW price
        time.sleep(1)

    print('| @@@@@@@@@@@\n')
