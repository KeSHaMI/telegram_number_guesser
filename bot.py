import random
from typing import Callable, Optional
from functools import partial

import telebot

from telebot.types import (
    Message, CallbackQuery
)

from settings import BOT_TOKEN
from keyboards import *  # Import everything


bot = telebot.TeleBot(BOT_TOKEN)
data = {}


def get_user_int_input(message: Message, handler: Callable[[Message, int], None]):
    try:
        user_input = int(message.text)
        handler(message, user_input)
    except ValueError:
        bot.send_message(message.chat.id, 'Please enter number')
        bot.register_next_step_handler(message, partial(get_user_int_input, handler=handler))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.send_message(
        message.chat.id,
        "Hi, let's play a number guesser game!\nI will select a random integer form 1 to 10 and you will guess it!",
        reply_markup=get_play_the_game_inline_keyboard('Play the game')
    )
    data[message.chat.id] = None


def handle_user_guess(message: Message, user_guess: Optional[int] = None):

    if user_guess is None:
        bot.send_message(message.chat.id, 'Enter your guess')
        handler = partial(get_user_int_input, handler=handle_user_guess)
        bot.register_next_step_handler(message, handler)
        return

    user_secret_number = data[message.chat.id]['secret_number']
    if user_guess == user_secret_number:
        bot.send_message(message.chat.id, 'You win', reply_markup=get_play_the_game_inline_keyboard('Play again'))
        return

    bot.send_message(message.chat.id, 'You loh')
    data[message.chat.id]['attempts_left'] -= 1
    if data[message.chat.id]['attempts_left'] < 1:
        bot.send_message(
            message.chat.id, 'You lose, no attempts left :(',
            reply_markup=get_play_the_game_inline_keyboard('Try one more time')
        )
        return

    handler = partial(get_user_int_input, handler=handle_user_guess)
    bot.register_next_step_handler(message, handler)


def handle_user_attempts(message: Message, user_attempts: Optional[int] = None):
    if user_attempts is None:
        bot.send_message(message.chat.id, 'Enter how many attempts you want')
        handler = partial(get_user_int_input, handler=handle_user_attempts)
        bot.register_next_step_handler(message, handler)
        return

    if user_attempts < 1:
        bot.send_message(
            message.chat.id, 'Come on, seriously, you need more than 0 attempts to guess a number, try one more time'
        )
        handler = partial(get_user_int_input, handler=handle_user_attempts)
        bot.register_next_step_handler(message, handler)
        return

    data[message.chat.id]['attempts_left'] = user_attempts
    handle_user_guess(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'start_guesser')
def start_game_handler(call: CallbackQuery):
    bot.send_message(call.message.chat.id, "Let's play")

    secret_number = random.randrange(1, 10)
    data[call.message.chat.id] = {'secret_number': secret_number, 'attempts_left': None}

    handle_user_attempts(call.message)


print('bot started')
bot.infinity_polling()
