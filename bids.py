#!/usr/bin/env python3

import time
import datetime

import bot
import queries

from binance.exceptions import BinanceAPIException

def cancel_current_best_offer(best_offer_price_, best_bid_price_):
    print(f'\n| ###{datetime.datetime.now().strftime("%H:%M")}###')
    print(f'| BID at price {best_bid_price_} was EXECUTED;')

    try:
        bot.CLIENT.cancel_order(symbol=bot.TRADING_PAIR, orderId=queries.get_order_id(best_offer_price_))  # CANCEL currentlly 'BEST OFFER'
        print(f'| Cancelling BEST OFFER: {best_offer_price_}')
    except BinanceAPIException:
        print('[!!!] Error while canceling BEST OFFER')

# A function for replacing the executed BID
def update_rel_to_best_bid(best_offer_price_, best_bid_price_):
    if not queries.order_active(best_offer_price_):  # If NEW best OFFER order is not already or yet present on the market
        print(f'| Placing NEW BEST OFFER at lower price: {best_offer_price_}')
        bot.CLIENT.order_limit_sell(symbol=bot.TRADING_PAIR, quantity=bot.COINS_PER_ORDER, price=best_offer_price_)  # Placing an OFFER (NEW best OFFER) at a WINDOW price
        time.sleep(1)
    
    if not queries.order_active(best_bid_price_):  # If NEW best BID order is not already or yet present on the market
        print(f'| Placing NEW BEST BID at lower price: {best_bid_price_}')
        bot.CLIENT.order_limit_buy(symbol=bot.TRADING_PAIR, quantity=bot.COINS_PER_ORDER, price=best_bid_price_)  # Replacing executed BID with NEW best BID
        time.sleep(1)

    print('| ########### \n')
