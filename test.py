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
        order_info = base.CLIENT.query_orders_info(order_id, trades=False)

        if order_info['status'][0] == 'closed':
            return False
        else:
            return True
    except:
        return True
