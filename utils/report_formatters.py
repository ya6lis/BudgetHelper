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
    msg = get_text('report_title', user_id=user_id).format(report.period_name)
    msg += get_text('report_period', user_id=user_id).format(report.start_date, report.end_date)
    msg += '─' * 30 + '\n\n'
    
    # Фінансова зведення
    msg += get_text('report_financial_summary', user_id=user_id) + '\n\n'
    msg += f"💰 {get_text('report_total_income', user_id=user_id)}: <b>{report.total_income:.2f} UAH</b>\n"
    msg += f"💸 {get_text('report_total_expense', user_id=user_id)}: <b>{report.total_expense:.2f} UAH</b>\n"
    
    # Баланс з індикатором
    if report.net_balance > 0:
        msg += f"📈 {get_text('report_balance', user_id=user_id)}: <b>+{report.net_balance:.2f} UAH</b>\n"
    elif report.net_balance < 0:
        msg += f"📉 {get_text('report_balance', user_id=user_id)}: <b>{report.net_balance:.2f} UAH</b>\n"
    else:
        msg += f"⚖️ {get_text('report_balance', user_id=user_id)}: <b>{report.net_balance:.2f} UAH</b>\n"
    
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
    msg = get_text('report_category_breakdown', user_id=user_id) + '\n\n'
    
    # Доходи по категоріях
    if report.income_by_category:
        msg += get_text('report_income_categories', user_id=user_id) + '\n'
        
        # Групуємо по основній категорії (до двокрапки)
        grouped_incomes = {}
        for category_key, amount in report.income_by_category.items():
            # Витягуємо основну категорію (до двокрапки)
            main_category = category_key.split(':')[0].strip() if ':' in category_key else category_key
            if main_category not in grouped_incomes:
                grouped_incomes[main_category] = 0
            grouped_incomes[main_category] += amount
        
        # Сортуємо категорії за сумою
        sorted_incomes = sorted(
            grouped_incomes.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Показуємо топ-N категорій
        top_categories = sorted_incomes[:top_n]
        other_categories = sorted_incomes[top_n:]
        
        for category_key, amount in top_categories:
            category_display = translate_category_name(category_key, user_id=user_id)
            percentage = (amount / report.total_income * 100) if report.total_income > 0 else 0
            msg += f"  • {category_display}: <b>{amount:.2f} UAH</b> (<b>{percentage:.2f}%</b>)\n"
        
        # Якщо є інші категорії, об'єднуємо їх
        if other_categories:
            other_total = sum(amount for _, amount in other_categories)
            other_percentage = (other_total / report.total_income * 100) if report.total_income > 0 else 0
            other_text = get_text('report_other_categories', user_id=user_id) or 'Інші категорії'
            msg += f"  • {other_text} ({len(other_categories)}): <b>{other_total:.2f} UAH</b> (<b>{other_percentage:.2f}%</b>)\n"
        
        msg += '\n'
    
    # Витрати по категоріях
    if report.expense_by_category:
        msg += get_text('report_expense_categories', user_id=user_id) + '\n'
        
        # Групуємо по основній категорії (до двокрапки)
        grouped_expenses = {}
        for category_key, amount in report.expense_by_category.items():
            # Витягуємо основну категорію (до двокрапки)
            main_category = category_key.split(':')[0].strip() if ':' in category_key else category_key
            if main_category not in grouped_expenses:
                grouped_expenses[main_category] = 0
            grouped_expenses[main_category] += amount
        
        # Сортуємо категорії за сумою
        sorted_expenses = sorted(
            grouped_expenses.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Показуємо топ-N категорій
        top_categories = sorted_expenses[:top_n]
        other_categories = sorted_expenses[top_n:]
        
        for category_key, amount in top_categories:
            category_display = translate_category_name(category_key, user_id=user_id)
            percentage = (amount / report.total_expense * 100) if report.total_expense > 0 else 0
            msg += f"  • {category_display}: <b>{amount:.2f} UAH</b> (<b>{percentage:.2f}%</b>)\n"
        
        # Якщо є інші категорії, об'єднуємо їх
        if other_categories:
            other_total = sum(amount for _, amount in other_categories)
            other_percentage = (other_total / report.total_expense * 100) if report.total_expense > 0 else 0
            other_text = get_text('report_other_categories', user_id=user_id) or 'Інші категорії'
            msg += f"  • {other_text} ({len(other_categories)}): <b>{other_total:.2f} UAH</b> (<b>{other_percentage:.2f}%</b>)\n"
        
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
    msg = get_text('report_statistics', user_id=user_id) + '\n'
    msg += f"📊 {get_text('report_transaction_count', user_id=user_id)}: <b>{report.transaction_count}</b>\n"
    msg += f"📥 {get_text('report_income_count', user_id=user_id)}: <b>{report.income_count}</b>\n"
    msg += f"📤 {get_text('report_expense_count', user_id=user_id)}: <b>{report.expense_count}</b>\n"
    
    if report.income_count > 0:
        msg += f"💰 {get_text('report_avg_income', user_id=user_id)}: <b>{report.avg_income:.2f} UAH</b>\n"
    if report.expense_count > 0:
        msg += f"💸 {get_text('report_avg_expense', user_id=user_id)}: <b>{report.avg_expense:.2f} UAH</b>\n"
    
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
    msg = f"⚡ {get_text('report_quick_summary', user_id=user_id)}\n"
    msg += f"📅 {report.start_date} — {report.end_date}\n\n"
    msg += f"💰 {get_text('report_total_income', user_id=user_id)}: <b>{report.total_income:.2f} UAH</b>\n"
    msg += f"💸 {get_text('report_total_expense', user_id=user_id)}: <b>{report.total_expense:.2f} UAH</b>\n"
    
    if report.net_balance >= 0:
        msg += f"📈 {get_text('report_balance', user_id=user_id)}: <b>+{report.net_balance:.2f} UAH</b>"
    else:
        msg += f"📉 {get_text('report_balance', user_id=user_id)}: <b>{report.net_balance:.2f} UAH</b>"
    
    return msg
