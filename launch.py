#!/usr/bin/env python3

import datetime
import sys

import bot
import queries

# A function for turning the float into a printable and understandable form
# (e.g 2.22e-05 to '0.0000222')
def _float_to_printable(num):
    num_str = str(num)
    
    # If the given float is of the form x.xxx...xxxe-xxx
    if 'e' in num_str:
        num_of_zeros = int(num_str[len(num_str) - 1]) - 1 # Number of zeros after comma
        e_index = num_str.index('e')
        decimals = num_str[0] + num_str[2:e_index]  # Numbers after zeros (e.g all xxx in 0.000...0xxx)
        printable_float = '0.' + '0' * num_of_zeros + decimals  # Combine the string float
        
        return printable_float
    else:
        return num_str
        
# A function for displaying the 'start_trading' initial interface
def start_trading_ui(asset_balance_free_, coin_balance_free_):

    print('\n**************************')
    print('Starting trading session:')
    print('--------------------------')
    print(f'Time: {datetime.datetime.now().strftime("%H:%M")}')
    print('--------------------------')
    print(f'Step: {bot.STEP_TO_PRINT}  {bot.TRADING_ASSET.lower()}')
    print(f'Spread: {bot.SPREAD_TO_PRINT} ({_float_to_printable(round(bot.SPREAD * bot.STEP, bot.NUM_DECIMAL_PLACES))}) {bot.TRADING_ASSET.lower()}')
    print(f'{bot.TRADING_COIN} per BID: {bot.COINS_PER_ORDER_TO_PRINT}')
    print('**************************\n')

    while True:
        start = input('Start trading(y/n): ')
        if start.lower() == 'y':
            break
        elif start.lower() == 'n':
            sys.exit()
        else:
            continue

    if not queries.enough_balance(asset_balance_free_, coin_balance_free_):  # If there is not enough balance to start trading
        print('\n| Not enough balance in asset or coin!')
        sys.exit()

# A fuction for placing the best BID and OFFER orders on the market
def place_init_orders(best_offer_price_, window_price_, best_bid_price_):
    if not queries.order_active(best_offer_price_):  # If the 'BEST OFFER' order is not already or yet present on the market
        print(f'| Placing BEST OFFER at: {best_offer_price_}')
        bot.CLIENT.order_limit_sell(symbol=bot.TRADING_PAIR, quantity=bot.COINS_PER_ORDER, price=best_offer_price_)

    if not queries.order_active(best_bid_price_):  # If the 'BEST BID' order is not already or yet present on the market
        print(f'| Placing BEST BID at: {best_bid_price_}')
        bot.CLIENT.order_limit_buy(symbol=bot.TRADING_PAIR, quantity=bot.COINS_PER_ORDER, price=best_bid_price_)
