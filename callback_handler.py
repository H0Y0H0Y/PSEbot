from telebot.types import ForceReply
import requests

from keyboard import (get_ph_stocks_markup, get_stock_markup,
                      get_back_markup)
from stock import Stock


def handle_select_action(bot, query):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    if query.data == 'psei':
        stock = Stock('PSEI')
        send_text = stock.get_stock_details()
        bot.edit_message_text(text=send_text, chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=get_stock_markup('PSEI'))

    if query.data == 'stock':
        send_text = "Input a stock ticker:"
        msg = bot.send_message(chat_id, text=send_text,
                               reply_markup=ForceReply())
        bot.register_next_step_handler(msg, _process_specified_stock, bot)


def handle_get_addtl_info(bot, query):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    action = query.data.split('_')[0]
    ticker = query.data.split('_')[1]
    markup = get_back_markup(ticker)
    stock = Stock(ticker)

    if action == 'more':
        send_text = stock.get_more_info()
        bot.edit_message_text(text=send_text, chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=markup)

    if action == 'fundamental':
        send_text = stock.get_fundamental()
        bot.edit_message_text(text=send_text, chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=markup)

    if action == 'technical':
        send_text = stock.get_technical()
        bot.edit_message_text(text=send_text, chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=markup)

    if action == 'back':
        send_text = "What do you want to do?"
        markup = get_ph_stocks_markup()
        bot.edit_message_text(text=send_text, chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=markup)


def _process_specified_stock(message, bot):
    ticker = message.text
    chat_id = message.chat.id
    if _stock_exists(ticker):
        stock = Stock(ticker.upper())
        send_text = stock.get_stock_details()
        bot.send_message(chat_id, text=send_text,
                         reply_markup=get_stock_markup(ticker.upper()))
    else:
        msg = bot.send_message(chat_id,
                               text="Please input a valid stock.",
                               reply_markup=ForceReply())
        bot.register_next_step_handler(msg, _process_specified_stock, bot)


def handle_get_back_to_stock_main(bot, query):
    message_id = query.message.message_id
    chat_id = query.message.chat.id
    ticker = query.data.split('_')[1]
    stock = Stock(ticker.upper())
    send_text = stock.get_stock_details()
    bot.edit_message_text(text=send_text, chat_id=chat_id,
                          message_id=message_id,
                          reply_markup=get_stock_markup(ticker.upper()))


def _stock_exists(stock):
    page = requests.get(f"https://www.investagrams.com/Stock/{stock}")
    # if page.history list is empty the page was not redirected
    # if page is not redirected, stock exists
    if not page.history:
        return True
    return False
