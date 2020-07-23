#!/usr/bin/env python3

# pip3 install -r requirements.txt

import time
import datetime
import json
import sys

import bids
import offers
import reports
import calc
import launch
import queries

from binance.client import Client

#========== Reading CONFIG file ==========#
with open('config.json', 'r') as config_file:  # Open and read the 'config.json' file
    config_data = json.load(config_file)
    
    #---------- Binance_bot data ----------#
    API_KEY = config_data['Binance_bot']['api_key']
    API_SECRET = config_data['Binance_bot']['api_secret']

    TRADING_ASSET = config_data['Binance_bot']['asset']  # Coin to trade against of (ex. BTC)
    TRADING_COIN = config_data['Binance_bot']['coin']  # Trading coin (ex. BNB)
    TRADING_PAIR = str(TRADING_COIN + TRADING_ASSET)  # Trading pair: BNB for BTC => BNBBTC

    SPREAD = int(config_data['Binance_bot']['spread'])  # Distance between: BID => OFFER in number of STEPS (see line below)
    SPREAD_TO_PRINT = config_data['Binance_bot']['spread']
    
    STEP = float(config_data['Binance_bot']['step'])  # Distance between: order(of any type) => order(of any type) in asset value
    STEP_TO_PRINT = config_data['Binance_bot']['step']

    COINS_PER_ORDER = float(config_data['Binance_bot']['coins_per_order'])  # Quantity of coins for one BID
    COINS_PER_ORDER_TO_PRINT = config_data['Binance_bot']['coins_per_order']
    
    #---------- Email_sender data ----------#
    SENDER_ADDRESS = config_data['Email_sender']['sender_address']
    SENDER_PASS = config_data['Email_sender']['sender_pass']
    
    RECEIVER_ADDRESS = config_data['Email_sender']['receiver_address']

#========== Connecting to API ==========#
CLIENT = Client(API_KEY, API_SECRET)  # Connecting to the Binance API

#========== Setting Up Constants ==========#
INIT_COIN_PRICE = queries.get_coin_price()  #  An initial coin price
NUM_DECIMAL_PLACES = calc.count_decimal_places()  # Round all prices to the constant number of decimal places

PRICES_ARR = calc.generate_grid_of_prices()  # An array of initial prices

#========== If ran as main ==========#
if __name__ == "__main__":

    #========== Setting UP ==========#
    current_day = datetime.datetime.now().strftime("%d")  # Current day of month
    current_week = datetime.datetime.now().strftime("%W")  # Current day of the week
    current_month = datetime.datetime.now().strftime("%b")  # Current month

    tmp_day = current_day  # Temporal variable for holding current day of month
    tmp_week = current_week  # Temporal variable for holding current day of the week
    tmp_month = current_month  # Temporal variable for holding current month

    asset_balance = CLIENT.get_asset_balance(asset=TRADING_ASSET)  # An array of info about the original balance
    asset_balance_free = float(asset_balance['free'])  # Original balance of free asset
    coin_balace = CLIENT.get_asset_balance(asset=TRADING_COIN)     #  An array of info about the original coin balance
    coin_balance_free = float(coin_balace['free'])  # Original balance of free coin

    window_price = calc.find_current_window_price()  # An empty window for BID/OFFER orders
    best_offer_price = calc.find_best_offer_price(window_price) # Current best OFFER
    best_bid_price = calc.find_best_bid_price(best_offer_price)  # Current best BID
        
    #========== Printing INFO ==========#
    launch.start_trading_ui(asset_balance_free, coin_balance_free)
    
    print('\n| ----------')
    print(f'| Best OFFER: {best_offer_price}')
    print(f'| WINDOW: {window_price}')
    print(f'| Best BID: {best_bid_price}')
    print('| ----------\n')

    #========== Placing Initial Orders ==========#
    launch.place_init_orders(best_offer_price, window_price, best_bid_price)

    #========== Trading Loop ==========#
    while True:  # The MAIN trading loop

        try:
            time.sleep(3)  # Each 10 seconds send requests to the market

            current_day = datetime.datetime.now().strftime("%d")  # Update the current day of month
            current_week = datetime.datetime.now().strftime("%W")  # Update the current day of the week
            current_month = datetime.datetime.now().strftime("%b")  # Update the current month

            if (not queries.order_active(best_offer_price) and queries.get_order_status(best_offer_price) == 'FILLED' 
                and queries.enough_balance(asset_balance_free, coin_balance_free)):  # If the current best-deal OFFER was executed and there is enough balance to continue
                
                offers.cancel_current_best_bid(best_offer_price, best_bid_price)  # Cancel current best BID
                
                window_price = calc.up_current_window_price(window_price)  # New empty window for BID/OFFER orders
                best_offer_price = calc.find_best_offer_price(window_price) # New best OFFER
                best_bid_price = calc.find_best_bid_price(best_offer_price)  # Current best BID

                offers.update_rel_to_best_offer(best_offer_price, best_bid_price)
                reports.save_order("SELL", best_offer_price)

                print('\n| ----------')
                print(f'| Best OFFER: {best_offer_price}')
                print(f'| WINDOW: {window_price}')
                print(f'| Best BID: {best_bid_price}')
                print('| ----------\n')

            if (not queries.order_active(best_bid_price) and queries.get_order_status(best_bid_price) == 'FILLED' 
                and queries.enough_balance(asset_balance_free, coin_balance_free)):  # If the current best-deal BID was executed and there is enough balance to continue
                
                bids.cancel_current_best_offer(best_offer_price, best_bid_price)    # Cancel current best OFFER
                
                window_price = calc.down_current_window_price(window_price)  # New empty window for BID/OFFER orders
                best_offer_price = calc.find_best_offer_price(window_price) # New best OFFER
                best_bid_price = calc.find_best_bid_price(best_offer_price)  # Current best BID

                bids.update_rel_to_best_bid(best_offer_price, best_bid_price)
                reports.save_order("BUY", best_bid_price)

                print('\n| ----------')
                print(f'| Best OFFER: {best_offer_price}')
                print(f'| WINDOW: {window_price}')
                print(f'| Best BID: {best_bid_price}')
                print('| ----------\n')

            if current_day != tmp_day:  # If day has passed
                
                #reports.daily_report(queries.num_closed_inday_offers(), calc.calc_asset_profit(queries.num_closed_inday_offers()))
                tmp_day = current_day
            
                #print('\n| Daily Report Generated\n')
            
            if current_week != tmp_week:  # If week has passed
                
                reports.weekly_report(queries.num_closed_inweek_offers(), calc.calc_asset_profit(queries.num_closed_inweek_offers()))
                tmp_week = current_week

                print('\n| Weekly Report Generated\n')
            
            if current_month != tmp_month:  # If month has passed

                #reports.monthly_report(queries.num_closed_inmonth_offers(), calc.calc_asset_profit(queries.num_closed_inmonth_offers()))
                tmp_month = current_month
            
                #print('\n| Monthly Report Generated\n')

            else:
                continue

        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:
            print(f'[!!!] [{datetime.datetime.now().strftime("%H:%M")}] {e}')
            with open('errors.log', 'a') as errors_log:
                errors_log.write(f'[{datetime.datetime.now().strftime("%d %b %Y; %H:%M")}] {e}\n')
            continue
