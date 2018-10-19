"""
Use this token to access the HTTP API:
573992100:AAE0JFkCFjlR2E6Mta7hBIuTLozfJqPzEC4
"""

import pandas as pd
import numpy as np
import sys
import os
import requests
from datetime import datetime, timedelta
import time

import sys
import asyncio
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.aio.delegate import (
    per_chat_id_in, per_application, call, create_open, pave_event_space)

token = '573992100:AAE0JFkCFjlR2E6Mta7hBIuTLozfJqPzEC4'
TeleBot = telepot.Bot(token)

# TeleBot.sendMessage(TeleBot.getUpdates().id, 'Hi')

# Loading CSVs
bf_path = os.path.abspath("menu_bf.csv")
din_path = os.path.abspath("menu_din.csv")

bf_menu = pd.read_csv(bf_path)
din_menu = pd.read_csv(din_path)

cur_date = datetime.now().date()
cur_day = cur_date.strftime('%A')
tmr_date = cur_date + timedelta(days=1)
tmr_day = tmr_date.strftime('%A')


# Define meal retriever
def get_meal(meal, data):
    msg = ''
    if data.empty:
        if meal == 'bf':
            return "There's no breakfast :("
        if meal == 'din':
            return "There's no dinner :("
    for i in range(2, len(data.iloc[0])):
        if data.iloc[0].values[i] is not np.nan:
            msg+='{}'.format(data.iloc[0].values[i])
            msg+='\n'
    return msg

def handle(msg):
    hello_msg = 'Hello {}! Which menu would you like to see?'.format(msg['chat']['first_name'])
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Breakfast', callback_data='bf')],
                    [InlineKeyboardButton(text='Dinner', callback_data='din')]
                ])
    bot.sendMessage(chat_id, hello_msg, reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    if (query_data == 'bf'):
        # breakfast
        cur_bf = bf_menu[bf_menu['Date']==str(cur_date)]
        tmr_bf = bf_menu[bf_menu['Date']==str(tmr_date)]
        
        bot.sendMessage(from_id, "{}'s breakfast:".format(cur_day))
        bot.sendMessage(from_id, get_meal('bf', cur_bf))
        bot.sendMessage(from_id, "{}'s breakfast:".format(tmr_day))
        bot.sendMessage(from_id, get_meal('bf', tmr_bf))
    elif (query_data == 'din'):
        # dinner
        cur_din = din_menu[din_menu['Date']==str(cur_date)]
        tmr_din = din_menu[din_menu['Date']==str(tmr_date)]

        bot.sendMessage(from_id, "{}'s dinner:".format(cur_day))
        bot.sendMessage(from_id, get_meal('din', cur_din))
        bot.sendMessage(from_id, "{}'s dinner:".format(tmr_day))
        bot.sendMessage(from_id, get_meal('din', tmr_din))

bot = telepot.Bot(token)
MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
