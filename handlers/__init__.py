# -*- coding: utf-8 -*-
"""
Пакет з обробниками повідомлень для Budget Helper бота.
"""

# Імпортуємо всі обробники для зручності
from . import start
from . import income
from . import finance
from . import misc

# Можна буде додати пізніше:
# from . import expenses
# from . import report
# from . import settings

__all__ = [
    'start',
    'income',
    'finance',
    'misc',
]
