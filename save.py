#!/usr/bin/env python3

import csv
import datetime

import base
import mail


# Save a record of a closed order
# --- in
# * str(order_type)
# * str(coin_price)
# --- out
# None
# -----------------
def order_record(order_type, coin_price):
    current_date_str = datetime.datetime.now().strftime("%d.%m.%Y")  # Current date
    current_month_str = datetime.datetime.now().strftime("%b")  # Current month
    current_year_str = datetime.datetime.now().strftime("%Y")  # Current year

    try:  # Try to create a new file, if it does not exists and write down the info
        with open('orders/' + current_month_str + '_' + current_year_str + '_orders.csv', 'x') as database:
            
            headers =['date', 'pair', 'type', 'price', 'coins']
            csv_writer = csv.DictWriter(database, headers)

            csv_writer.writeheader()
    except FileExistsError:
        pass
    
    # However if the file already exists, then open it in 'append' mode
    with open('orders/' + current_month_str + '_' + current_year_str + '_orders.csv', 'a') as database:
            
        headers =['date', 'pair', 'type', 'price', 'coins']
        csv_writer = csv.DictWriter(database, headers)
             
        csv_writer.writerow({'date': current_date_str, 'pair': base.TRADING_PAIR, 'type': order_type, 'price': coin_price, 'coins': base.LOT})


# Generate and mail a daily report
# --- in
# * int(num_closed_spreads)
# --- out
# None
# -----------------
def daily_report(num_closed_spreads):
    current_date = datetime.datetime.now()  # Current date
    day_before_date = current_date - datetime.timedelta(days=1)  # Date a day before
    
    day_before_date_str = day_before_date.strftime("%d.%m.%Y")
    
    report_name = day_before_date_str + '_daily.csv'
    report_path = 'reports/daily/' + report_name
    
    asset_profit = float(round(num_closed_spreads * (base.SPREAD * base.STEP * base.LOT), base.DECIMAL_PLACES))
    
    with open(report_path, 'w') as database:
            
        headers =['date', 'closed', 'profit']
        csv_writer = csv.DictWriter(database, headers)

        csv_writer.writeheader()
            
        csv_writer.writerow({'date':day_before_date_str, 'closed':str(num_closed_spreads), 'profit':str(asset_profit)})
        print('\n| Daily Report was Generated\n')
    
    try:  # Try to send the generated report via email
        mail.regular_report('Daily', str(report_path), str(report_name), str(day_before_date_str))
        print('\n| Daily Report was Sent\n')
        
    except FileNotFoundError:
        print('[!!!] Cannot send the email: Report does not exists')
    
    except:
        print('[!!!] Cannot send the email: Unexpected Error')


# Generate and save a weekly report
# --- in
# * int(num_closed_spreads)
# --- out
# None
# -----------------
def weekly_report(num_closed_spreads):
    current_date = datetime.datetime.now()  # Current date
    week_before_date = current_date - datetime.timedelta(days=7)  # Date a week before

    current_date_str = current_date.strftime("%d.%m.%Y")
    week_before_date_str = week_before_date.strftime("%d.%m.%Y")
    
    report_name = week_before_date_str + '_' + current_date_str + '_weekly.csv'
    report_path = 'reports/weekly/' + report_name

    asset_profit = float(round(num_closed_spreads * (base.SPREAD * base.STEP * base.LOT), base.DECIMAL_PLACES))

    with open(report_path, 'w') as database:
            
        headers =['date', 'closed', 'profit']
        csv_writer = csv.DictWriter(database, headers)

        csv_writer.writeheader()
            
        csv_writer.writerow({'date':current_date_str, 'closed':str(num_closed_spreads), 'profit':str(asset_profit)})
        print('\n| Weekly Report was Generated\n')
        
    try:  # Try to send the generated report via email
        mail.regular_report('Weekly', str(report_path), str(report_name), str(week_before_date_str + '-' + current_date_str))
        print('\n| Weekly Report was just Sent\n')
        
    except FileNotFoundError:
        print('[!!!] Cannot send the email: Report does not exists')
    
    except:
        print('[!!!] Cannot send the email: Unexpected Error')


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


# Generate and save a monthly report
# --- in
# * int(num_closed_spreads)
# --- out
# None
# -----------------
def monthly_report(num_closed_spreads):
    current_date = datetime.datetime.now()  # Current date
    month_before_date = current_date.replace(month=_get_past_month_num())  # Date a month before
    
    current_date_str = current_date.strftime("%d.%m.%Y")
    month_before_date_str = month_before_date.strftime("%b.%Y")
    
    report_name = month_before_date_str + '_monthly.csv'
    report_path = 'reports/monthly/' + report_name

    asset_profit = float(round(num_closed_spreads * (base.SPREAD * base.STEP * base.LOT), base.DECIMAL_PLACES))

    with open(report_path, 'w') as database:
            
        headers =['date', 'closed', 'profit']
        csv_writer = csv.DictWriter(database, headers)

        csv_writer.writeheader()
            
        csv_writer.writerow({'date': current_date_str, 'closed':str(num_closed_spreads), 'profit':str(asset_profit)})
        print('\n| Monthly Report was Generated\n')
        
    try:  # Try to send the generated report via email
        mail.regular_report('Monthly', str(report_path), str(report_name), month_before_date_str)
        print('\n| Monthly Report was just Sent\n')
        
    except FileNotFoundError:
        print('[!!!] Cannot send the email: Report does not exists')
    
    except:
        print('[!!!] Cannot send the email: Unexpected Error')
