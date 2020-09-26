#!/usr/bin/env python3

import datetime

import base


# Get current asset balance that is free to be utilized in trading
# --- in
# None
# --- out
# * float(free_asset_balance)
# -----------------
def free_asset_balance():
    asset_balance = base.CLIENT.get_asset_balance(asset=base.TRADING_ASSET)       # Array of data about original asset balance
    free_asset_balance = float(asset_balance['free'])                   # Original balance of free asset

    return free_asset_balance


# Get current coin balance that is free to be utilized in trading
# --- in
# None
# --- out
# * float(free_coin_balance)
# -----------------
def free_coin_balance():
    coin_balace = base.CLIENT.get_asset_balance(asset=base.TRADING_COIN)          # Array of data about original coin balance
    free_coin_balance = float(coin_balace['free'])                      # Original balance of free coin

    return free_coin_balance


# Convert server-time to datetime object
# --- in
# * float(timestamp)
# --- out
# * fromtimestamp()
# -----------------
def _timestamp_to_date(timestamp):
    global CLIENT

    return datetime.datetime.fromtimestamp(timestamp/1000)


# Count IDs of orders closed within last 24h
# --- in
# None
# --- out
# * int(count)
# -----------------
def num_closed_inday_offers():
    server_time = _timestamp_to_date(base.CLIENT.get_server_time()['serverTime'])  # 'To' date
    from_date = server_time - datetime.timedelta(days=1)  # 'From' date

    orders_arr = base.CLIENT.get_all_orders(symbol=base.TRADING_PAIR, limit=500)
    decimal_places = len(str(base.LOT).split('.')[1])

    count = 0
    for order in orders_arr:
        if (order['status'] == 'FILLED' and order['side'] == 'SELL' and round(float(order['origQty']), decimal_places) == base.LOT
                and (from_date < _timestamp_to_date(order['updateTime']) < server_time)):

            count += 1
    
    return count


# Count IDs of orders closed within a week
# --- in
# None
# --- out
# * int(count)
# -----------------
def num_closed_inweek_offers():
    server_time = _timestamp_to_date(base.CLIENT.get_server_time()['serverTime'])  # 'To' date
    from_date = server_time - datetime.timedelta(days=7)  # 'From' date

    orders_arr = base.CLIENT.get_all_orders(symbol=base.TRADING_PAIR, limit=500)
    decimal_places = len(str(base.LOT).split('.')[1])
    
    count = 0
    for order in orders_arr:
        if (order['status'] == 'FILLED' and order['side'] == 'SELL' and round(float(order['origQty']), decimal_places) == base.LOT
            and (from_date < _timestamp_to_date(order['updateTime']) < server_time)):

            count += 1
    
    return count
    

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


# Count IDs of orders, closed within a month
# --- in
# None
# --- out
# * int(count)
# -----------------
def num_closed_inmonth_offers():
    server_time = _timestamp_to_date(base.CLIENT.get_server_time()['serverTime'])  # 'To' date
    month_before_date = server_time.replace(month=_get_past_month_num())  # Date a month before

    orders_arr = base.CLIENT.get_all_orders(symbol=base.TRADING_PAIR, limit=500)
    decimal_places = len(str(base.LOT).split('.')[1])

    count = 0
    for order in orders_arr:
        if (order['status'] == 'FILLED' and order['side'] == 'SELL' and round(float(order['origQty']), decimal_places) == base.LOT
            and (month_before_date < _timestamp_to_date(order['updateTime']) < server_time)):
        
            count += 1
    
    return count
