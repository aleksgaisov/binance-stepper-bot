#!/usr/bin/env python3

import datetime

import bot

# A function to get the price of a certain coin
def get_coin_price():
    current_coin_price = float(bot.CLIENT.get_ticker(symbol=bot.TRADING_PAIR)['askPrice'])
    
    return current_coin_price

# A function to get the id of the order at a certain price
def get_order_id(coin_price):
    orders_arr = bot.CLIENT.get_open_orders(symbol=bot.TRADING_PAIR)  # An array of active orders for the currentlly trading coin
    
    for order in orders_arr:
        if round(float(order['price']), bot.NUM_DECIMAL_PLACES) == coin_price:
            return order['orderId']  # Returns the order id
        else:
            continue

# A function to get the status of the order at a certain price            
def get_order_status(coin_price):
    orders_arr = bot.CLIENT.get_all_orders(symbol=bot.TRADING_PAIR, limit=2)
    
    for order in orders_arr:
        if round(float(order['price']), bot.NUM_DECIMAL_PLACES) == coin_price:
            return order['status']
        else:
            continue
    else:
        return None

# A function to check whether an order at a certain price is present on the market
def order_active(coin_price):
    orders_arr = bot.CLIENT.get_open_orders(symbol=bot.TRADING_PAIR)  # An array of active orders for the currentlly trading coin

    for order in orders_arr:
        if round(float(order['price']), bot.NUM_DECIMAL_PLACES) == coin_price:
            return True
    else:
        return False

# A function to check if there is enough balance in both, asset and coin for one more order
def enough_balance(asset_balance_free_, coin_balance_free_): 
    if (asset_balance_free_ >= bot.COINS_PER_ORDER * get_coin_price() and 
        coin_balance_free_ >= bot.COINS_PER_ORDER):
        
        return True
    else:
        return False
        
# A function to convert the server-time to the datetime object
def timestamp_to_date(timestamp):
    global CLIENT

    return datetime.datetime.fromtimestamp(float(timestamp)/1000)
     
# A function to count the IDs of orders, closed within last 24h
def num_closed_inday_offers():
    server_time = timestamp_to_date(bot.CLIENT.get_server_time()['serverTime'])  # 'To' date
    from_date = server_time - datetime.timedelta(days=1)  # 'From' date

    orders_arr = bot.CLIENT.get_all_orders(symbol=bot.TRADING_PAIR, limit=500)
    decimal_places = len(str(bot.COINS_PER_ORDER).split('.')[1])
    
    count = 0
    for order in orders_arr:
        if (order['status'] == 'FILLED' and order['side'] == 'SELL' and round(float(order['origQty']), decimal_places) == bot.COINS_PER_ORDER
            and (from_date < timestamp_to_date(order['updateTime']) < server_time)):

            count += 1
    
    return count


# A function to count the IDs of orders, closed within last week
def num_closed_inweek_offers():
    server_time = timestamp_to_date(bot.CLIENT.get_server_time()['serverTime'])  # 'To' date
    from_date = server_time - datetime.timedelta(days=7)  # 'From' date

    orders_arr = bot.CLIENT.get_all_orders(symbol=bot.TRADING_PAIR, limit=500)
    decimal_places = len(str(bot.COINS_PER_ORDER).split('.')[1])
    
    count = 0
    for order in orders_arr:
        if (order['status'] == 'FILLED' and order['side'] == 'SELL' and round(float(order['origQty']), decimal_places) == bot.COINS_PER_ORDER
            and (from_date < timestamp_to_date(order['updateTime']) < server_time)):

            count += 1
    
    return count
    
# A function for getting the number of the previous month (ex. dec=12 => return nov=11)        
def _get_past_month_num():
    current_month_num = int(datetime.datetime.now().strftime("%m"))  # Get the current number of a month (1 - 12)
    
    if current_month_num == 1:
        return 12
    else:
        return current_month_num - 1

# A function to count the IDs of orders, closed within last month
def num_closed_inmonth_offers():
    server_time = timestamp_to_date(bot.CLIENT.get_server_time()['serverTime'])  # 'To' date
    month_before_date = server_time.replace(month=_get_past_month_num())  # Date a month before

    orders_arr = bot.CLIENT.get_all_orders(symbol=bot.TRADING_PAIR, limit=500)
    decimal_places = len(str(bot.COINS_PER_ORDER).split('.')[1])

    count = 0
    for order in orders_arr:
        if (order['status'] == 'FILLED' and order['side'] == 'SELL' and round(float(order['origQty']), decimal_places) == bot.COINS_PER_ORDER
            and (month_before_date < timestamp_to_date(order['updateTime']) < server_time)):
        
            count += 1
    
    return count
