#!/usr/bin/env python3

import time
import datetime
import sys

import base
import grab
import test


# Convert a float into a printable and understandable form
# (e.x 2.22e-05 to '0.0000222')
# --- in
# * str(num)
# --- out
# str(printable_float)
# -----------------
def _float_to_printable(num):
    num = str(num)
    
    # If the given float is of the form x.xxx...xxxe-xxx
    if 'e' in num:
        num_of_zeros = int(num[len(num) - 1]) - 1 # Number of zeros after comma
        e_index = num.index('e')
        decimals = num[0] + num[2:e_index]  # Numbers after zeros (e.g all xxx in 0.000...0xxx)
        printable_float = '0.' + '0' * num_of_zeros + decimals  # Combine the string float
        
        return printable_float
    else:
        return num
        

# Print out a starting trade info
# (this is for user ot confirm the values and prompt to start trading)
# --- in
# None
# --- out
# None
# -----------------
def out_trading_info():

    print('\n**************************')
    print('Starting trading session:')
    print('--------------------------')
    print(f'Time: {datetime.datetime.now().strftime("%H:%M")}')
    print('--------------------------')
    print(f'Step: {_float_to_printable(base.STEP)} {base.TRADING_ASSET}')
    print(f'Spread: {base.SPREAD} ({_float_to_printable(round((1 + base.SPREAD) * base.STEP, base.DECIMAL_PLACES))}) {base.TRADING_ASSET}')
    print(f'{base.TRADING_COIN} per order: {base.LOT}')
    print('--------------------------')
    print(f'MAIL_DAILY_REPORTS: {base.MAIL_DAILY_REPORTS}')
    print(f'MAIL_WEEKLY_REPORTS: {base.MAIL_WEEKLY_REPORTS}')
    print(f'MAIL_MONTHLY_REPORTS: {base.MAIL_MONTHLY_REPORTS}')
    print('**************************\n')

    while True:
        try:
            start = input('Start trading(y/n): ')
            if start.lower() == 'y':
                break
            elif start.lower() == 'n':
                sys.exit()
            else:
                continue

        except KeyboardInterrupt:
            print('')
            sys.exit()


# Send an order to the market
# --- in
# * str(order_type)
# * str(order_price)
# --- out
# * str(order_id)
# -----------------
def base_order(order_type, order_price):
    try: 
        response = base.CLIENT.add_standard_order(base.TRADING_PAIR,    # pair
                                                  order_type,           # type 
                                                  'limit',              # ordertype 
                                                  str(base.LOT),        # vol 
                                                  order_price,          # price 
                                                  validate=False)       # allow order to be send 
    except:
        print('| Config values are invalid')
        sys.exit()


    order_id = response['txid'][0]  # Save a unique ID current order was sent with
    time.sleep(1)  # Delay to avoid "public call frequency exceeded" error

    return str(order_id)


# Cancel a certain order 
# --- in
# * str(order_id)
# --- out
# None
# -----------------
def cancel_order(order_id):
    try:
       base.CLIENT.cancel_open_order(order_id)
    except:
        print('| Noting to cancel')
