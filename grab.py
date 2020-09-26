#!/usr/bin/env python3

import datetime
import time

import base


# Get current asset balance that is free to be utilized in trading
# --- in
# None
# --- out
# * float(asset_balance)
# -----------------
def asset_balance():
    asset_balance = base.CLIENT.get_account_balance()['vol']['X' + base.TRADING_ASSET]  # Array of data about original asset balance

    time.sleep(1)  # Delay to avoid "public call frequency exceeded" error

    return float(asset_balance)


# Get current coin balance that is free to be utilized in trading
# --- in
# None
# --- out
# * float(coin_balance)
# -----------------
def coin_balance():
    coin_balance = base.CLIENT.get_account_balance()['vol']['X' + base.TRADING_COIN]  # Array of data about original coin balance

    time.sleep(1)  # Delay to avoid "public call frequency exceeded" error

    return float(coin_balance)


# Convert server-time to datetime object
# --- in
# * float(timestamp)
# --- out
# * datetime()
# -----------------
def _timestamp_to_date(timestamp):
    global CLIENT

    return datetime.datetime.fromtimestamp(timestamp)


# Count orders closed within last 24h
# --- in
# None
# --- out
# * int(count)
# -----------------
def num_closed_inday_offers():
    server_time = int(base.CLIENT.get_server_time()[1])
    from_date = _timestamp_to_date(server_time) - datetime.timedelta(days=1)
    from_date = int(from_date.timestamp())

    orders_arr = base.CLIENT.get_closed_orders(trades=False, start=int(from_date), end=int(server_time), closetime=None)[0]
    decimal_places = len(str(base.LOT).split('.')[1])

    count = 0
    for i in range(0, len(orders_arr)):
        if (orders_arr['status'][i] == 'closed' and orders_arr['descr_type'][i] == 'sell'
            and round(float(orders_arr['vol'][i]), decimal_places) == base.LOT):

            count += 1

    time.sleep(1)  # Delay to avoid "public call frequency exceeded" error
    
    return int(count)


# Count orders closed within a week
# --- in
# None
# --- out
# * int(count)
# -----------------
def num_closed_inweek_offers():
    server_time = int(base.CLIENT.get_server_time()[1])
    from_date = _timestamp_to_date(server_time) - datetime.timedelta(days=7)
    from_date = int(from_date.timestamp())

    orders_arr = base.CLIENT.get_closed_orders(trades=False, start=int(from_date), end=int(server_time), closetime=None)[0]
    decimal_places = len(str(base.LOT).split('.')[1])

    count = 0
    for i in range(0, len(orders_arr)):
        if (orders_arr['status'][i] == 'closed' and orders_arr['descr_type'][i] == 'sell'
            and round(float(orders_arr['vol'][i]), decimal_places) == base.LOT):

            count += 1

    time.sleep(1)  # Delay to avoid "public call frequency exceeded" error
    
    return int(count)
    

# Get the number of the previous month 
# (ex. dec=12 => return nov=11)        
# --- in
# None
# --- out
# * int(current_month_num) or 12
# -----------------
def _get_past_month_num():
    current_month_num = int(datetime.datetime.now().strftime("%m"))  # Get the current number of a month (1 - 12)
    
    if current_month_num == 1:
        return 12
    else:
        return current_month_num - 1


# Count orders, closed within a month
# --- in
# None
# --- out
# * int(count)
# -----------------
def num_closed_inmonth_offers():
    server_time = int(base.CLIENT.get_server_time()[1])
    month_before_date = _timestamp_to_date(server_time).replace(month=_get_past_month_num())  # Date a month before
    month_before_date = int(month_before_date.timestamp())

    orders_arr = base.CLIENT.get_closed_orders(trades=False, start=int(from_date), end=int(server_time), closetime=None)[0]
    decimal_places = len(str(base.LOT).split('.')[1])

    count = 0
    for i in range(0, len(orders_arr)):
        if (orders_arr['status'][i] == 'closed' and orders_arr['descr_type'][i] == 'sell'
            and round(float(orders_arr['vol'][i]), decimal_places) == base.LOT):

            count += 1

    time.sleep(1)  # Delay to avoid "public call frequency exceeded" error
    
    return int(count)
