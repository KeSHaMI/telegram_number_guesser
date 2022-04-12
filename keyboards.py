from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_play_the_game_inline_keyboard(button_text: str):
    keyboard = InlineKeyboardMarkup()
    but = InlineKeyboardButton(button_text, callback_data='start_guesser')
    keyboard.add(but)
    return keyboard

