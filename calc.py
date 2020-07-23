#!/usr/bin/env python3

import bot

# A function to generate the grid of prices for future orders
def generate_grid_of_prices():    
    up_to_price = bot.INIT_COIN_PRICE * 10;  # Generate array up to this price 
    grid_arr = []
    order_price = 0  # A starting price
    
    while order_price < up_to_price:  # While the generated price is still smaller than the maximum possible price
        grid_arr.append(round(order_price, bot.NUM_DECIMAL_PLACES)) # Append a new price to the array of prices
        order_price = round(order_price + bot.STEP, bot.NUM_DECIMAL_PLACES)  # Add the STEP value to the future price
    
    return grid_arr

# A function for finding the current WINDOW price
def find_current_window_price():
    for price in bot.PRICES_ARR: # Iterate through the array of prices
        if price >= bot.INIT_COIN_PRICE: #  If the price is larger than the current price
            return price
            break;
        else:
            continue;
    
    return None;

def find_best_offer_price(window_price_):
    window_price_i = bot.PRICES_ARR.index(window_price_)  # Index value of a window price
    
    if bot.SPREAD % 2 == 0:  # If SPREAD is even
        return bot.PRICES_ARR[window_price_i + int(bot.SPREAD / 2)]  # Return the value whose index is half SPREAD higher than the WINDOW price
    else:  # If SPREAD is odd
        return bot.PRICES_ARR[window_price_i + (int(bot.SPREAD / 2) + 1)]  # Return the value whose index is one SPREAD higher than the WINDOW price
    
def find_best_bid_price(offer_price):
    offer_price_i = bot.PRICES_ARR.index(offer_price)  # Index value of a window price
    
    return bot.PRICES_ARR[offer_price_i - (bot.SPREAD + 1)]  # Return the value whose index is SPREAD + 1 lower than the OFFER price
    
def up_current_window_price(window_price_):
    return bot.PRICES_ARR[bot.PRICES_ARR.index(window_price_) + 1]  # + 1 STEP (adding 1 to index, but the next value is 1 STEP larger)
    
def down_current_window_price(window_price_):
    return bot.PRICES_ARR[bot.PRICES_ARR.index(window_price_) - 1]  # - 1 STEP (subtracting 1 from index, but the previous value is 1 STEP lower)
    
def count_decimal_places():
    init_coin_price_str = str(bot.INIT_COIN_PRICE)

    return int(init_coin_price_str[::-1].find('.'))  # Count all simbols until meeting a '.'

# A function for calculating the profit
def calc_asset_profit(num_closed_spreads):
    asset_profit = float(round(num_closed_spreads * (bot.SPREAD * bot.STEP * bot.COINS_PER_ORDER), bot.NUM_DECIMAL_PLACES))

    return asset_profit
