#!/usr/bin/env python3

import base


# Finding the current WINDOW price
# (the first price in ORDER_PRICES that is larger than the current coin price)
# --- in
# * float(coin_price)
# --- out
# * float(price)
# -----------------
def current_window_price(coin_price):
    for price in base.ORDER_PRICES:  # Iterate through the array of prices
        if price >= coin_price:  # If the the price is larger than the current price
            return price
        else:
            continue
    

# Finding the current best OFFER price
# (price in ORDER_PRICES that is above the WINDOW price, based on SPREAD value)
# --- in
# * float(window_price_)
# --- out
# * float()
# -----------------
def best_offer_price(window_price_):
    window_price_i = base.ORDER_PRICES.index(window_price_)  # Index value of a window price
    
    if base.SPREAD % 2 == 0:  # If SPREAD is even
        return base.ORDER_PRICES[window_price_i + int(base.SPREAD / 2)]  # Return the value whose index is half SPREAD higher than the WINDOW price
    else:  # If SPREAD is odd
        return base.ORDER_PRICES[window_price_i + (int(base.SPREAD / 2) + 1)]  # Return the value whose index is one SPREAD higher than the WINDOW price
    

# Finding the current best BID price
# (Price in ORDER_PRICES that is below the WINDOW price, based on SPREAD value)
# --- in
# * float(offer_price)
# --- out
# * float()
# -----------------
def best_bid_price(offer_price):
    offer_price_i = base.ORDER_PRICES.index(offer_price)  # Index value of a window price
    
    return base.ORDER_PRICES[offer_price_i - (base.SPREAD + 1)]  # Return the value whose index is SPREAD + 1 lower than the OFFER price
    

# Move WINDOW price value UP
# (up one index in ORDER_PRICES array)
# --- in
# * float(window_price_)
# --- out
# * float()
# -----------------
def higher_window_price(window_price_):
    return base.ORDER_PRICES[base.ORDER_PRICES.index(window_price_) + 1]  # +1 index
    

# Move WINDOW price value DOWN
# (down one index in ORDER_PRICES array)
# --- in
# * float(window_price_)
# --- out
# * float()
# -----------------
def lower_window_price(window_price_):
    return base.ORDER_PRICES[base.ORDER_PRICES.index(window_price_) - 1]  # -1 index
