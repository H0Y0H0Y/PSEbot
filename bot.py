import configparser

import telebot

from keyboard import get_ph_stocks_markup
from callback_handler import (handle_select_action,
                              handle_get_addtl_info,
                              handle_get_back_to_stock_main)


config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('DEFAULT', 'token')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    send_text = "Hi! This bot shows data " \
                "and real time prices of stocks listed in PSE\n" \
                "Data comes from Investagrams\n" \
                "Visit the site: https://www.investagrams.com/\n\n" \
                "Use /phstocks command to display options"
    bot.send_message(message.chat.id, text=send_text)


@bot.message_handler(commands=['phstocks'])
def phstocks(message):
    send_text = "What do you want to do?"
    markup = get_ph_stocks_markup()
    bot.send_message(message.chat.id, text=send_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda query: query.data in
                            ['psei', 'stock'])
def select_action(query):
    handle_select_action(bot, query)


@bot.callback_query_handler(func=lambda query:
                            query.data.split('_')[0]
                            in ['more', 'fundamental', 'technical', 'back'])
def get_addtl_info(query):
    handle_get_addtl_info(bot, query)


@bot.callback_query_handler(func=lambda query:
                            query.data.split('_')[0] == 'backMain')
def get_back_to_stock_main(query):
    handle_get_back_to_stock_main(bot, query)


if __name__ == '__main__':
    bot.polling()
