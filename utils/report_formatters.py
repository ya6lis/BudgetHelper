# -*- coding: utf-8 -*-
"""
Форматери для звітів та аналізу бюджету.
"""

from typing import Dict
from locales import get_text, translate_category_name
from models import ReportData, PeriodComparison


def format_detailed_report(report: ReportData, user_id: int = None) -> str:
    """
    Форматує детальний звіт для Telegram.
    
    Args:
        report: Об'єкт ReportData
        user_id: ID користувача для локалізації
    
    Returns:
        str: Відформатований текст звіту
    """
    from utils.currency_converter import get_currency_symbol
    
    currency_symbol = get_currency_symbol(report.currency)
    
    msg = get_text('report_title', user_id=user_id).format(report.period_name)
    msg += get_text('report_period', user_id=user_id).format(report.start_date, report.end_date)
    msg += '─' * 30 + '\n\n'
    
    # Перевіряємо чи є кілька валют
    all_currencies = set()
    if report.income_by_currency:
        all_currencies.update(report.income_by_currency.keys())
    if report.expense_by_currency:
        all_currencies.update(report.expense_by_currency.keys())
    
    # Фінансова зведення
    msg += get_text('report_financial_summary', user_id=user_id) + '\n\n'
    
    # Доходи
    msg += f"💰 {get_text('report_total_income', user_id=user_id)}: <b>≈ {report.total_income:.2f} {currency_symbol}</b>\n"
    if report.income_by_currency and len(report.income_by_currency) > 0:
        for curr, amount in report.income_by_currency.items():
            curr_symbol = get_currency_symbol(curr)
            if curr == report.currency:
                msg += f"    • {amount:.2f} {curr_symbol}\n"
            else:
                from utils.currency_converter import convert_currency
                converted = convert_currency(amount, curr, report.currency)
                msg += f"    • {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
    
    # Витрати
    msg += f"💸 {get_text('report_total_expense', user_id=user_id)}: <b>≈ {report.total_expense:.2f} {currency_symbol}</b>\n"
    if report.expense_by_currency and len(report.expense_by_currency) > 0:
        for curr, amount in report.expense_by_currency.items():
            curr_symbol = get_currency_symbol(curr)
            if curr == report.currency:
                msg += f"    • {amount:.2f} {curr_symbol}\n"
            else:
                from utils.currency_converter import convert_currency
                converted = convert_currency(amount, curr, report.currency)
                msg += f"    • {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
    
    # Баланс з індикатором та розбивкою
    balance_icon = "📈" if report.net_balance > 0 else ("📉" if report.net_balance < 0 else "⚖️")
    balance_sign = "+" if report.net_balance > 0 else ""
    msg += f"{balance_icon} {get_text('report_balance', user_id=user_id)}: <b>{balance_sign}{report.net_balance:.2f} {currency_symbol}</b>\n"
    
    # Розбивка балансу по валютах
    if report.income_by_currency and report.expense_by_currency:
        # Рахуємо баланс для кожної валюти
        all_balance_currencies = set(list(report.income_by_currency.keys()) + list(report.expense_by_currency.keys()))
        if len(all_balance_currencies) > 0:
            for curr in sorted(all_balance_currencies):
                income_amt = report.income_by_currency.get(curr, 0)
                expense_amt = report.expense_by_currency.get(curr, 0)
                balance_amt = income_amt - expense_amt
                
                if balance_amt != 0:  # Показуємо тільки якщо є баланс
                    curr_symbol = get_currency_symbol(curr)
                    balance_sign_curr = "+" if balance_amt > 0 else ""
                    
                    if curr == report.currency:
                        msg += f"    • {balance_sign_curr}{balance_amt:.2f} {curr_symbol}\n"
                    else:
                        from utils.currency_converter import convert_currency
                        converted = convert_currency(abs(balance_amt), curr, report.currency)
                        converted_signed = converted if balance_amt > 0 else -converted
                        msg += f"    • {balance_sign_curr}{balance_amt:.2f} {curr_symbol} <i>(≈ {'+' if converted_signed > 0 else ''}{converted_signed:.2f} {currency_symbol})</i>\n"
    
    msg += '\n'
    
    # Розбивка по категоріях
    if report.income_by_category or report.expense_by_category:
        msg += format_category_breakdown(report, user_id)
    
    # Статистика
    msg += format_statistics(report, user_id)
    
    # Порівняння з попереднім періодом
    if report.previous_period:
        msg += format_period_comparison(report.previous_period, user_id)
    
    return msg


def format_category_breakdown(report: ReportData, user_id: int = None, top_n: int = 10) -> str:
    """
    Форматує розбивку по категоріях з обмеженням на кількість.
    Групує по основній категорії (без підкатегорій), сортує за процентами.
    Показує топ-N категорій, решту об'єднує в "Інші категорії".
    
    Args:
        report: Об'єкт ReportData
        user_id: ID користувача для локалізації
        top_n: Кількість топ-категорій для відображення (за замовчуванням 10)
    
    Returns:
        str: Відформатований текст розбивки
    """
    from utils.currency_converter import get_currency_symbol
    
    currency_symbol = get_currency_symbol(report.currency)
    msg = get_text('report_category_breakdown', user_id=user_id) + '\n\n'
    
    # Доходи по категоріях
    if report.income_by_category:
        msg += get_text('report_income_categories', user_id=user_id) + '\n'
        
        # Використовуємо aggregated_by_category_currency якщо є, інакше звичайний aggregated
        if report.income_by_category_currency:
            # Сортуємо категорії за загальною сумою (конвертованою)
            sorted_incomes = sorted(
                report.income_by_category.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            top_categories = sorted_incomes[:top_n]
            other_categories = sorted_incomes[top_n:]
            
            for category_key, converted_amount in top_categories:
                category_display = translate_category_name(category_key, user_id=user_id)
                percentage = (converted_amount / report.total_income * 100) if report.total_income > 0 else 0
                
                # Показуємо оригінальні валюти
                currencies = report.income_by_category_currency.get(category_key, {})
                if currencies:
                    # Якщо є кілька валют або валюта не дефолтна, показуємо кожну окремо
                    if len(currencies) > 1 or report.currency not in currencies:
                        msg += f"  • {category_display}:\n"
                        for curr, amount in sorted(currencies.items()):
                            curr_symbol = get_currency_symbol(curr)
                            if curr != report.currency:
                                from utils.currency_converter import convert_currency
                                converted = convert_currency(amount, curr, report.currency)
                                msg += f"    ◦ {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
                            else:
                                msg += f"    ◦ {amount:.2f} {curr_symbol}\n"
                        total_text = get_text('total_text', user_id=user_id)
                        msg += f"    <b>{total_text}: ≈ {converted_amount:.2f} {currency_symbol} ({percentage:.2f}%)</b>\n"
                    else:
                        # Одна валюта (дефолтна)
                        curr = list(currencies.keys())[0]
                        amount = currencies[curr]
                        curr_symbol = get_currency_symbol(curr)
                        msg += f"  • {category_display}: <b>{amount:.2f} {curr_symbol}</b> <b>({percentage:.2f}%)</b>\n"
        else:
            # Старий формат (без розбивки по валютах)
            grouped_incomes = {}
            for category_key, amount in report.income_by_category.items():
                main_category = category_key.split(':')[0].strip() if ':' in category_key else category_key
                if main_category not in grouped_incomes:
                    grouped_incomes[main_category] = 0
                grouped_incomes[main_category] += amount
            
            sorted_incomes = sorted(grouped_incomes.items(), key=lambda x: x[1], reverse=True)
            top_categories = sorted_incomes[:top_n]
            other_categories = sorted_incomes[top_n:]
            
            for category_key, amount in top_categories:
                category_display = translate_category_name(category_key, user_id=user_id)
                percentage = (amount / report.total_income * 100) if report.total_income > 0 else 0
                msg += f"  • {category_display}: <b>{amount:.2f} {currency_symbol}</b> (<b>{percentage:.2f}%</b>)\n"
        
        # Якщо є інші категорії, об'єднуємо їх
        if 'other_categories' in locals() and other_categories:
            other_total = sum(amount for _, amount in other_categories)
            other_percentage = (other_total / report.total_income * 100) if report.total_income > 0 else 0
            other_text = get_text('report_other_categories', user_id=user_id) or 'Інші категорії'
            msg += f"  • {other_text} ({len(other_categories)}): <b>{other_total:.2f} {currency_symbol}</b> (<b>{other_percentage:.2f}%</b>)\n"
        
        msg += '\n'
    
    # Витрати по категоріях
    if report.expense_by_category:
        msg += get_text('report_expense_categories', user_id=user_id) + '\n'
        
        # Використовуємо aggregated_by_category_currency якщо є, інакше звичайний aggregated
        if report.expense_by_category_currency:
            # Сортуємо категорії за загальною сумою (конвертованою)
            sorted_expenses = sorted(
                report.expense_by_category.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            top_categories = sorted_expenses[:top_n]
            other_categories = sorted_expenses[top_n:]
            
            for category_key, converted_amount in top_categories:
                category_display = translate_category_name(category_key, user_id=user_id)
                percentage = (converted_amount / report.total_expense * 100) if report.total_expense > 0 else 0
                
                # Показуємо оригінальні валюти
                currencies = report.expense_by_category_currency.get(category_key, {})
                if currencies:
                    # Якщо є кілька валют або валюта не дефолтна, показуємо кожну окремо
                    if len(currencies) > 1 or report.currency not in currencies:
                        msg += f"  • {category_display}:\n"
                        for curr, amount in sorted(currencies.items()):
                            curr_symbol = get_currency_symbol(curr)
                            if curr != report.currency:
                                from utils.currency_converter import convert_currency
                                converted = convert_currency(amount, curr, report.currency)
                                msg += f"    ◦ {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
                            else:
                                msg += f"    ◦ {amount:.2f} {curr_symbol}\n"
                        total_text = get_text('total_text', user_id=user_id)
                        msg += f"    <b>{total_text}: ≈ {converted_amount:.2f} {currency_symbol} ({percentage:.2f}%)</b>\n"
                    else:
                        # Одна валюта (дефолтна)
                        curr = list(currencies.keys())[0]
                        amount = currencies[curr]
                        curr_symbol = get_currency_symbol(curr)
                        msg += f"  • {category_display}: <b>{amount:.2f} {curr_symbol}</b> <b>({percentage:.2f}%)</b>\n"
        else:
            # Старий формат (без розбивки по валютах)
            grouped_expenses = {}
            for category_key, amount in report.expense_by_category.items():
                main_category = category_key.split(':')[0].strip() if ':' in category_key else category_key
                if main_category not in grouped_expenses:
                    grouped_expenses[main_category] = 0
                grouped_expenses[main_category] += amount
            
            sorted_expenses = sorted(grouped_expenses.items(), key=lambda x: x[1], reverse=True)
            top_categories = sorted_expenses[:top_n]
            other_categories = sorted_expenses[top_n:]
            
            for category_key, amount in top_categories:
                category_display = translate_category_name(category_key, user_id=user_id)
                percentage = (amount / report.total_expense * 100) if report.total_expense > 0 else 0
                msg += f"  • {category_display}: <b>{amount:.2f} {currency_symbol}</b> (<b>{percentage:.2f}%</b>)\n"
        
        # Якщо є інші категорії, об'єднуємо їх
        if 'other_categories' in locals() and other_categories:
            other_total = sum(amount for _, amount in other_categories)
            other_percentage = (other_total / report.total_expense * 100) if report.total_expense > 0 else 0
            other_text = get_text('report_other_categories', user_id=user_id) or 'Інші категорії'
            msg += f"  • {other_text} ({len(other_categories)}): <b>{other_total:.2f} {currency_symbol}</b> (<b>{other_percentage:.2f}%</b>)\n"
        
        msg += '\n'
    
    return msg


def format_statistics(report: ReportData, user_id: int = None) -> str:
    """
    Форматує статистичну інформацію.
    
    Args:
        report: Об'єкт ReportData
        user_id: ID користувача для локалізації
    
    Returns:
        str: Відформатована статистика
    """
    from utils.currency_converter import get_currency_symbol
    
    currency_symbol = get_currency_symbol(report.currency)
    
    msg = get_text('report_statistics', user_id=user_id) + '\n'
    msg += f"📊 {get_text('report_transaction_count', user_id=user_id)}: <b>{report.transaction_count}</b>\n"
    msg += f"📥 {get_text('report_income_count', user_id=user_id)}: <b>{report.income_count}</b>\n"
    msg += f"📤 {get_text('report_expense_count', user_id=user_id)}: <b>{report.expense_count}</b>\n"
    
    # Середній дохід з розбивкою по валютах
    if report.income_count > 0:
        msg += f"💰 {get_text('report_avg_income', user_id=user_id)}: <b>≈ {report.avg_income:.2f} {currency_symbol}</b>\n"
        
        if report.income_by_currency and len(report.income_by_currency) > 0:
            for curr, total_amount in report.income_by_currency.items():
                # Рахуємо кількість доходів в цій валюті
                income_count_in_currency = sum(1 for inc in report.incomes if getattr(inc, 'currency', 'UAH') == curr)
                if income_count_in_currency > 0:
                    avg_amount = total_amount / income_count_in_currency
                    curr_symbol = get_currency_symbol(curr)
                    
                    if curr == report.currency:
                        msg += f"    • {avg_amount:.2f} {curr_symbol}\n"
                    else:
                        from utils.currency_converter import convert_currency
                        converted = convert_currency(avg_amount, curr, report.currency)
                        msg += f"    • {avg_amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
    
    # Середня витрата з розбивкою по валютах
    if report.expense_count > 0:
        msg += f"💸 {get_text('report_avg_expense', user_id=user_id)}: <b>≈ {report.avg_expense:.2f} {currency_symbol}</b>\n"
        
        if report.expense_by_currency and len(report.expense_by_currency) > 0:
            for curr, total_amount in report.expense_by_currency.items():
                # Рахуємо кількість витрат в цій валюті
                expense_count_in_currency = sum(1 for exp in report.expenses if getattr(exp, 'currency', 'UAH') == curr)
                if expense_count_in_currency > 0:
                    avg_amount = total_amount / expense_count_in_currency
                    curr_symbol = get_currency_symbol(curr)
                    
                    if curr == report.currency:
                        msg += f"    • {avg_amount:.2f} {curr_symbol}\n"
                    else:
                        from utils.currency_converter import convert_currency
                        converted = convert_currency(avg_amount, curr, report.currency)
                        msg += f"    • {avg_amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
    
    msg += '\n'
    return msg


def format_period_comparison(comparison: PeriodComparison, user_id: int = None) -> str:
    """
    Форматує порівняння з попереднім періодом.
    
    Args:
        comparison: Об'єкт PeriodComparison
        user_id: ID користувача для локалізації
    
    Returns:
        str: Відформатоване порівняння
    """
    msg = get_text('report_comparison_title', user_id=user_id) + '\n'
    
    # Зміна доходів
    if comparison.income_change > 0:
        msg += f"📈 {get_text('report_income_change', user_id=user_id)}: <b>+{comparison.income_change:.2f} UAH</b> (<b>+{comparison.income_change_percent:.2f}%</b>)\n"
    elif comparison.income_change < 0:
        msg += f"📉 {get_text('report_income_change', user_id=user_id)}: <b>{comparison.income_change:.2f} UAH</b> (<b>{comparison.income_change_percent:.2f}%</b>)\n"
    else:
        msg += f"➡️ {get_text('report_income_change', user_id=user_id)}: {get_text('no_change', user_id=user_id)}\n"
    
    # Зміна витрат
    if comparison.expense_change > 0:
        msg += f"📈 {get_text('report_expense_change', user_id=user_id)}: <b>+{comparison.expense_change:.2f} UAH</b> (<b>+{comparison.expense_change_percent:.2f}%</b>)\n"
    elif comparison.expense_change < 0:
        msg += f"📉 {get_text('report_expense_change', user_id=user_id)}: <b>{comparison.expense_change:.2f} UAH</b> (<b>{comparison.expense_change_percent:.2f}%</b>)\n"
    else:
        msg += f"➡️ {get_text('report_expense_change', user_id=user_id)}: {get_text('no_change', user_id=user_id)}\n"
    
    # Зміна балансу
    if comparison.balance_change > 0:
        msg += f"✅ {get_text('report_balance_improved', user_id=user_id)}: <b>+{comparison.balance_change:.2f} UAH</b>\n"
    elif comparison.balance_change < 0:
        msg += f"⚠️ {get_text('report_balance_worsened', user_id=user_id)}: <b>{comparison.balance_change:.2f} UAH</b>\n"
    
    msg += '\n'
    return msg


def format_compact_report(report: ReportData, user_id: int = None) -> str:
    """
    Форматує компактний звіт (швидкий огляд).
    
    Args:
        report: Об'єкт ReportData
        user_id: ID користувача для локалізації
    
    Returns:
        str: Короткий звіт
    """
    from utils.currency_converter import get_currency_symbol
    
    currency_symbol = get_currency_symbol(report.currency)
    
    msg = f"⚡ {get_text('report_quick_summary', user_id=user_id)}\n"
    msg += f"📅 {report.start_date} — {report.end_date}\n\n"
    msg += f"💰 {get_text('report_total_income', user_id=user_id)}: <b>{report.total_income:.2f} {currency_symbol}</b>\n"
    msg += f"💸 {get_text('report_total_expense', user_id=user_id)}: <b>{report.total_expense:.2f} {currency_symbol}</b>\n"
    
    if report.net_balance >= 0:
        msg += f"📈 {get_text('report_balance', user_id=user_id)}: <b>+{report.net_balance:.2f} {currency_symbol}</b>"
    else:
        msg += f"📉 {get_text('report_balance', user_id=user_id)}: <b>{report.net_balance:.2f} {currency_symbol}</b>"
    
    return msg
