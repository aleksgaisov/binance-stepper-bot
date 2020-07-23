#!/usr/bin/env python3

import datetime
import csv

import bot
import send

# A function for constructing the daily report in a '.csv' file
def daily_report(num_closed_spreads, asset_profit):
    current_date = datetime.datetime.now()  # Current date
    day_before_date = current_date - datetime.timedelta(days=1)  # Date a day before
    
    day_before_date_str = day_before_date.strftime("%d.%m.%Y")
    
    report_name = day_before_date_str + '_daily.csv'
    report_path = 'reports/daily/' + report_name
    
    with open(report_path, 'w') as database:
            
        headers =['date', 'closed', 'profit']
        csv_writer = csv.DictWriter(database, headers)

        csv_writer.writeheader()
            
        csv_writer.writerow({'date':day_before_date_str, 'closed':str(num_closed_spreads), 'profit':str(asset_profit)})
    
    try:  # Try to send the generated report via email
        send.send_daily_report(report_name, day_before_date_str)
        print('\n| Daily Report has been Sent\n')
        
    except FileNotFoundError:
        print('[!!!] Cannot send the email: Report does not exists')
        
    except:
        print('[!!!] Cannot send the email: Unexpected Error')

# A function for constructing the weekly report in a '.csv' file
def weekly_report(num_closed_spreads, asset_profit):
    current_date = datetime.datetime.now()  # Current date
    week_before_date = current_date - datetime.timedelta(days=7)  # Date a week before

    current_date_str = current_date.strftime("%d.%m.%Y")
    week_before_date_str = week_before_date.strftime("%d.%m.%Y")
    
    report_name = week_before_date_str + '_' + current_date_str + '_weekly.csv'
    report_path = 'reports/weekly/' + report_name

    with open(report_path, 'w') as database:
            
        headers =['date', 'closed', 'profit']
        csv_writer = csv.DictWriter(database, headers)

        csv_writer.writeheader()
            
        csv_writer.writerow({'date':current_date_str, 'closed':str(num_closed_spreads), 'profit':str(asset_profit)})
        
    try:  # Try to send the generated report via email
        send.send_weekly_report(report_name, week_before_date_str + '-' + current_date_str)
        print('\n| Weekly Report has been Sent\n')
        
    except FileNotFoundError:
        print('[!!!] Cannot send the email: Report does not exists')
        
    except:
        print('[!!!] Cannot send the email: Unexpected Error')

# A function for getting the number of the previous month (ex. dec=12 => return nov=11)        
def _get_past_month_num():
    current_month_num = int(datetime.datetime.now().strftime("%m"))  # Get the current number of a month (1 - 12)
    
    if current_month_num == 1:
        return 12
    else:
        return current_month_num - 1

# A function for constructing the monthly report in a '.csv' file
def monthly_report(num_closed_spreads, asset_profit):
    current_date = datetime.datetime.now()  # Current date
    month_before_date = current_date.replace(month=_get_past_month_num())  # Date a month before
    
    current_date_str = current_date.strftime("%d.%m.%Y")
    month_before_date_str = month_before_date.strftime("%b.%Y")
    
    report_name = month_before_date_str + '_monthly.csv'
    report_path = 'reports/monthly/' + report_name

    with open(report_path, 'w') as database:
            
        headers =['date', 'closed', 'profit']
        csv_writer = csv.DictWriter(database, headers)

        csv_writer.writeheader()
            
        csv_writer.writerow({'date': current_date_str, 'closed':str(num_closed_spreads), 'profit':str(asset_profit)})
        
    try:  # Try to send the generated report via email
        send.send_monthly_report(report_name, month_before_date_str)
        print('\n| Monthly Report has been Sent\n')
        
    except FileNotFoundError:
        print('[!!!] Cannot send the email: Report does not exists')
        
    except:
        print('[!!!] Cannot send the email: Unexpected Error')

# A function for saving all closed BIDS and OFFERS
def save_order(type_, coin_price):
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
             
        csv_writer.writerow({'date': current_date_str, 'pair': bot.TRADING_PAIR, 'type': type_, 'price': str(coin_price), 'coins': bot.COINS_PER_ORDER_TO_PRINT})
