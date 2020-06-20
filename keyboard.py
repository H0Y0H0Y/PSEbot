from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ph_stocks_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    show_psei = InlineKeyboardButton("Show PSEI",
                                     callback_data="psei")
    input_stock = InlineKeyboardButton("Specify a stock",
                                       callback_data="stock")
    markup.add(show_psei, input_stock)
    return markup


def get_stock_markup(stock):
    markup = InlineKeyboardMarkup(row_width=1)
    more_info = InlineKeyboardButton("More Info",
                                     callback_data=f"more_{stock}")
    fundamental = InlineKeyboardButton("Fundamental",
                                       callback_data=f"fundamental_{stock}")
    technical = InlineKeyboardButton("Technical",
                                     callback_data=f"technical_{stock}")
    back = InlineKeyboardButton("◀️", callback_data=f"back_{stock}")
    markup.add(more_info, fundamental, technical, back)
    return markup


def get_back_markup(stock):
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton("◀️", callback_data=f"backMain_{stock}")
    markup.add(back)
    return markup
