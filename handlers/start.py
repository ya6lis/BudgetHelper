# -*- coding: utf-8 -*-

from utils import send_main_menu
from locales import get_text


def register_handlers(bot):
    @bot.message_handler(commands=['start', 'help'])
    def welcome(message):
        send_main_menu(bot, message.chat.id, 'welcome')
