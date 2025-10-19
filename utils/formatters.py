# -*- coding: utf-8 -*-

from locales import get_text


def format_income_list(incomes, period, period_name):
    msg = get_text('view_incomes_title').format(period_name)
    total_income = 0

    if period == 'today':
        for inc in incomes:
            msg += f"— {inc['description']} : {inc['amount']:.2f} грн\n"
            total_income += inc['amount']
    else:
        for inc in incomes:
            msg += f"— {inc['description']} : {inc['total_amount']:.2f} грн\n"
            total_income += inc['total_amount']

    msg += get_text('view_incomes_total').format(total_income)
    return msg


def format_expense_list(expenses, period, period_name):
    msg = get_text('view_expenses_title').format(period_name)
    total_expense = 0

    if period == 'today':
        for exp in expenses:
            msg += f"— {exp['description']} : {exp['amount']:.2f} грн\n"
            total_expense += exp['amount']
    else:
        for exp in expenses:
            msg += f"— {exp['description']} : {exp['total_amount']:.2f} грн\n"
            total_expense += exp['total_amount']

    msg += get_text('view_expenses_total').format(total_expense)
    return msg


def format_amount(amount, currency='грн'):
    return f"{amount:.2f} {currency}"


def calculate_balance(incomes, expenses):
    return incomes - expenses
