# -*- coding: utf-8 -*-

from utils import send_main_menu
from locales import get_text


def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text in [
        get_text('menu_add_expense'),
        get_text('menu_view_general_finances'),
        get_text('menu_report'),
        get_text('menu_settings'),
        get_text('menu_view_expenses'),
    ])
    def handle_not_ready(message):
        send_main_menu(bot, message.chat.id, 'feature_not_ready')
