#!/usr/bin/env python3

import base
import grab


# Test if a certain order is active on the market
# --- in
# * str(order_id)
# --- out
# True or False
# -----------------
def order_active(order_id):
    try:
        order_info = base.CLIENT.get_order(symbol=base.TRADING_PAIR, 
                                           origClientOrderId=order_id)

        if order_info['status'] == 'FILLED':
            return False
        else:
            return True
    except:
        return True
