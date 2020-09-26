#!/usr/bin/env python3

# pip3 install -r requirements.txt

#  -------------------------
# |     Importing Libs      |
#  -------------------------

import datetime
import sys
import time
import random
import string

import find
import grab
import mail
import save
import send
import test

from binance.client import Client


#  -------------------------
# |     Base Functions      |
#  -------------------------

# Get current coin price
# --- in 
# None
# --- out 
# * float(current_coin_price)
# -----------------
def _coin_price():
    # Query current coin price
    current_coin_price = float(CLIENT.get_ticker(symbol=TRADING_PAIR)['askPrice'])
    
    return float(current_coin_price) 


# Calculate appropriate number of decimal places
# (based on the current coin price)
# --- in 
# * str(coin_price)    
# --- out 
# * int(num_dec_plc)    
# -----------------
def _decimal_places(coin_price):
    num_dec_plc = int(coin_price[::-1].find('.'))  # Count all symbols until meeting a '.'

    return num_dec_plc


# Generate array of prices based on the STEP value
# (predefined prices for orders to be placed at)
# --- in 
# * float(coin_price)    
# --- out 
# * list(orders_arr)
# -----------------
def _generate_order_prices(coin_price):    
    up_to_price = coin_price * 5;  # Generate array up to this price 
    orders_arr = []
    order_price = 0  # A starting price

    # While the generated price is still smaller than the maximum possible price
    while order_price < up_to_price:  
        orders_arr.append(round(order_price, DECIMAL_PLACES))  # Append a new price to the array of prices
        order_price = round(order_price + STEP, DECIMAL_PLACES)  # Add the STEP value to the future price
    
    return orders_arr


# Check if you have enough balace to trade
# (in both coins)
# --- in 
# * float(free_asset_balance_)
# * float(free_coin_balance_)
# --- out 
# True or False
# -----------------
def _enough_balance(free_asset_balance_, free_coin_balance_): 
    if (free_asset_balance_ >= LOT * _coin_price() and  # Is there enough coins to place at least one order
        free_coin_balance_ >= LOT):
        return True
    else:
        return False


# Generate a unique order id
# (in both coins)
# --- in 
# * int(id_len)
# --- out 
# * str(order_id)
# -----------------
def _generate_order_id(id_len):
    order_id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(id_len))

    return order_id


# Send BUY and SELL orders on the market
# (also, check if they are not already there)
# --- in 
# * float(best_offer_price_)
# * float(best_bid_price_)
# * str(best_offer_id_)
# * str(best_bid_id_)
# --- out 
# None
# -----------------
def _send_base_orders(best_offer_price_, best_bid_price_, best_offer_id_, best_bid_id_):
    print(f'| Placing best OFFER at price: {best_offer_price_}')
    send.base_order('SELL', str(best_offer_price_), best_offer_id_)  # Send current best OFFER

    time.sleep(1)  # Delay

    print(f'| Placing best BID at price: {best_bid_price_}')
    send.base_order('BUY', str(best_bid_price_), best_bid_id_)  # Send current bet BID


#  -------------------------
# |   Constant Variables    |
#  -------------------------

#===== Config Values =====#
API_KEY                 = str('') 
API_SECRET              = str('')

TRADING_COIN            = str('')                       # Trading coin (ex. BNB)
TRADING_ASSET           = str('')                       # Coin to trade against of (ex. BTC)
STEP                    = float()                       # Distance between BUY (BID) and SELL (OFFER) orders in asset value
SPREAD                  = int()                         # Distance between BID <=> OFFER in number of STEPS
LOT                     = float()                       # Quantity of coins per order

MAIL_DAILY_REPORTS      = bool(True)                    # If you want daily generated reports to be send to your email 
MAIL_WEEKLY_REPORTS     = bool(True)                    # If you want weekly generated reports to be send to your email 
MAIL_MONTHLY_REPORTS    = bool(True)                    # If you want monthly generated reports to be send to your email 

SENDER_ADDRESS          = str('')                       # From email
SENDER_PASS             = str('')                       # Email password
RECEIVER_ADDRESS        = str('')                       # To email


#  -------------------------
# |   Trading Variables     |
#  -------------------------

#===== Connecting to API =====#
CLIENT = Client(API_KEY, API_SECRET)  # Connecting to the Binance API

#===== Market Values =====#
TRADING_PAIR = TRADING_COIN + TRADING_ASSET  # Trading pair (ex. BNB for BTC => BNBBTC)
DECIMAL_PLACES = _decimal_places(str(_coin_price()))  # Round all order prices to a constant number of decimal places
ORDER_PRICES = _generate_order_prices(float(_coin_price()))  # Array of order prices


#  -------------------------
# |        Variables        |
#  -------------------------

if __name__ == "__main__":

    #===== Date Values =====#
    current_day = datetime.datetime.now().strftime("%d")  # Current day of month
    current_week = datetime.datetime.now().strftime("%W")  # Current day of the week
    current_month = datetime.datetime.now().strftime("%b")  # Current month

    tmp_day = current_day  # Temporal variable for holding current day of month
    tmp_week = current_week  # Temporal variable for holding current day of the week
    tmp_month = current_month  # Temporal variable for holding current month

    #===== Trading Values =====#
    window_price = find.current_window_price(float(_coin_price()))  # Middle price between BID and OFFER
    best_offer_price = find.best_offer_price(float(window_price))  # Current best OFFER
    best_bid_price = find.best_bid_price(float(best_offer_price))  # Current best BID

    best_offer_id = _generate_order_id(16)  # A unique identificator for OFFER
    best_bid_id = _generate_order_id(16)  # A unique identificator for BID
        
    #===== Init Trading =====#
    # If there is not enough balance to start trading
    if not _enough_balance(float(grab.free_asset_balance()), float(grab.free_coin_balance())):  
        print('\n| Not enough balance in asset or coin!')
        sys.exit()

    send.out_trading_info()  # Print start trading info
    
    print('\n| ----------')
    print(f'| Best OFFER: {best_offer_price}')
    print(f'| WINDOW: {window_price}')
    print(f'| Best BID: {best_bid_price}')
    print('| ----------\n')

    # Send both, best OFFER and best BID on the market
    _send_base_orders(str(best_offer_price), str(best_bid_price), str(best_offer_id), str(best_bid_id))
    print('')


    #  -------------------------
    # |       Trading Loop      |
    #  -------------------------

    #===== Main trading loop =====#
    while True:

        try:
            time.sleep(5)  # Delay

            current_day = datetime.datetime.now().strftime("%d")  # Update the current day of month
            current_week = datetime.datetime.now().strftime("%W")  # Update the current day of the week
            current_month = datetime.datetime.now().strftime("%b")  # Update the current month
            
            # If current OFFER is FILLED
            if not test.order_active(best_offer_id):
                # Check if we have enough in asset and coin
                # (we do not need to bother placing new orders if we do not have enough balace)
                if _enough_balance(float(grab.free_asset_balance()), float(grab.free_coin_balance())):
                    print(f'| @@@{datetime.datetime.now().strftime("%H:%M")}@@@')
                    print(f'| OFFER at price {best_offer_price} is Filled')

                    save.order_record('SELL', str(best_offer_price))  # Save the record about closed OFFER

                    print(f'| Cancelling BID at: {best_bid_price}')
                    send.cancel_order(str(best_bid_id))  # Cancel the pair BID (if still on the market)

                    window_price = find.higher_window_price(float(window_price))  # Move one index up in ORDER_PRICES array
                    best_offer_price = find.best_offer_price(float(window_price))  # New updated best OFFER price
                    best_bid_price = find.best_bid_price(float(best_offer_price))  # New updated best BID price

                    best_offer_id = _generate_order_id(16)  # New unique identificator for OFFER
                    best_bid_id = _generate_order_id(16)  # New unique identificator for BID

                    # Send new OFFER and BID on the market
                    _send_base_orders(str(best_offer_price), str(best_bid_price), str(best_offer_id), str(best_bid_id))

                    print('| @@@@@@@@@@@')

                    print('\n| ----------')
                    print(f'| Best OFFER: {best_offer_price}')
                    print(f'| WINDOW: {window_price}')
                    print(f'| Best BID: {best_bid_price}')
                    print('| ----------\n')

            # If current BID is FILLED
            if not test.order_active(best_bid_id): 
                # Check if we have enough in asset and coin
                # (we do not need to bother placing new orders if we do not have enough balace)
                if _enough_balance(float(grab.free_asset_balance()), float(grab.free_coin_balance())):
                    print(f'| ###{datetime.datetime.now().strftime("%H:%M")}###')
                    print(f'| BID at price {best_bid_price} is Filled')

                    save.order_record('BUY', str(best_bid_price))  # Save the record about closed BID

                    print(f'| Cancelling OFFER at: {best_offer_price}')
                    send.cancel_order(str(best_offer_id))  # Cancel the pair BID (if still on the market)

                    window_price = find.lower_window_price(float(window_price))  # Move one index down in ORDER_PRICES array
                    best_offer_price = find.best_offer_price(float(window_price))  # New updated best OFFER price
                    best_bid_price = find.best_bid_price(float(best_offer_price))  # New updated best BID price

                    best_offer_id = _generate_order_id(16)  # New unique identificator for OFFER
                    best_bid_id = _generate_order_id(16)  # New unique identificator for BID

                    # Send new OFFER and BID on the market
                    _send_base_orders(str(best_offer_price), str(best_bid_price), str(best_offer_id), str(best_bid_id))

                    print('| ###########')

                    print('\n| ----------')
                    print(f'| Best OFFER: {best_offer_price}')
                    print(f'| WINDOW: {window_price}')
                    print(f'| Best BID: {best_bid_price}')
                    print('| ----------\n')

            if current_day != tmp_day:  # If day has passed
                # Update the value to start a new countdown
                tmp_day = current_day

                if MAIL_DAILY_REPORTS:
                    # Generage a daily report and send via email (if selected)
                    save.daily_report(int(grab.num_closed_inday_offers()))

            if current_week != tmp_week:  # If week has passed
                # Update the value to start a new countdown
                tmp_week = current_week

                if MAIL_WEEKLY_REPORTS:
                    # Generage a weekly report and send via email (if selected)
                    save.weekly_report(int(grab.num_closed_inweek_offers()))

            if current_month != tmp_month:  # If month has passed
                # Update the value to start a new countdown
                tmp_month = current_month

                if MAIL_MONTHLY_REPORTS:
                    # Generage a monthly report and send via email (if selected)
                    save.monthly_report(int(grab.num_closed_inmonth_offers()))

            else:
                continue

        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:
            print(f'[!!!] [{datetime.datetime.now().strftime("%H:%M")}] {e}')
            with open('errors.log', 'a') as errors_log:
                errors_log.write(f'[{datetime.datetime.now().strftime("%d %b %Y; %H:%M")}] {e}\n')
            continue
