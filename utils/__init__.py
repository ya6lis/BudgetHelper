# -*- coding: utf-8 -*-
"""
Utilities package - допоміжні функції для Budget Helper.
Включає форматери, валідатори та helpers для повідомлень.
"""

from .message_helpers import (
    send_main_menu,
    send_back_button,
    send_with_keyboard,
    answer_callback,
    create_inline_keyboard_from_dict,
    edit_or_send_message,
)
from .validation import (
    validate_amount,
    is_back_command,
)
from .formatters import (
    format_income_list,
    format_expense_list,
    format_amount,
    calculate_balance,
    format_income_model,
    format_expense_model,
    format_general_finances,
)
from .report_formatters import (
    format_detailed_report,
    format_compact_report,
    format_category_breakdown,
    format_statistics,
    format_period_comparison,
)
from .html_report_generator import (
    generate_html_report,
    HTMLReportGenerator,
)

__all__ = [
    # Message Helpers
    'send_main_menu',
    'send_back_button',
    'send_with_keyboard',
    'answer_callback',
    'create_inline_keyboard_from_dict',
    'edit_or_send_message',
    
    # Validation
    'validate_amount',
    'is_back_command',
    
    # Formatters
    'format_income_list',
    'format_expense_list',
    'format_amount',
    'calculate_balance',
    'format_income_model',
    'format_expense_model',
    'format_general_finances',
    
    # Report Formatters
    'format_detailed_report',
    'format_compact_report',
    'format_category_breakdown',
    'format_statistics',
    'format_period_comparison',
    
    # HTML Report Generator
    'generate_html_report',
    'HTMLReportGenerator',
]

