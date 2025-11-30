# -*- coding: utf-8 -*-
"""
HTML Report Generator - генерація інтерактивних HTML звітів.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Optional
from models import ReportData
from locales import get_text, translate_category_name


class HTMLReportGenerator:
    """Генератор HTML звітів з графіками та таблицями."""
    
    def __init__(self, template_dir: str = 'templates'):
        """
        Ініціалізація генератора.
        
        Args:
            template_dir: Директорія з шаблонами Jinja2
        """
        self.template_dir = Path(template_dir)
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        self.output_dir = Path('reports')
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_report(
        self,
        report_data: ReportData,
        user_id: int,
        lang: str = 'uk'
    ) -> str:
        """
        Генерує HTML звіт.
        
        Args:
            report_data: Дані звіту
            user_id: ID користувача
            lang: Мова звіту
        
        Returns:
            str: Шлях до згенерованого HTML файлу
        """
        # Підготовка даних для шаблону
        template_data = self._prepare_template_data(report_data, user_id, lang)
        
        # Рендеринг шаблону
        template = self.env.get_template('report.html')
        html_content = template.render(**template_data)
        
        # Збереження файлу
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'report_{user_id}_{timestamp}.html'
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _prepare_template_data(
        self,
        report: ReportData,
        user_id: int,
        lang: str
    ) -> Dict:
        """
        Підготовка даних для Jinja2 шаблону.
        
        Args:
            report: Дані звіту
            user_id: ID користувача
            lang: Мова
        
        Returns:
            dict: Дані для шаблону
        """
        # Базова інформація
        data = {
            'lang': lang,
            'title': get_text('report_title', user_id=user_id).format(report.period_name),
            'period_text': get_text('report_period_text', user_id=user_id),
            'start_date': report.start_date,
            'end_date': report.end_date,
            'generation_date': datetime.now().strftime('%d.%m.%Y %H:%M'),
        }
        
        # Метрики
        data.update({
            'total_income': f"{report.total_income:.2f}",
            'total_expense': f"{report.total_expense:.2f}",
            'balance': f"{report.net_balance:.2f}",
            'balance_value': report.net_balance,  # Числове значення для порівняння
            'income_count': report.income_count,
            'expense_count': report.expense_count,
        })
        
        # Порівняння з попереднім періодом
        if report.previous_period:
            comp = report.previous_period
            data['income_change'] = comp.income_change
            data['income_change_percent'] = f"{comp.income_change_percent:.2f}"
            data['expense_change'] = comp.expense_change
            data['expense_change_percent'] = f"{comp.expense_change_percent:.2f}"
        
        # Тексти інтерфейсу
        data.update(self._get_interface_texts(user_id))
        
        # Дані категорій (спрощені - тільки основні категорії)
        data['income_data'] = self._prepare_category_data(
            report.income_by_category,
            report.total_income,
            user_id
        )
        
        data['expense_data'] = self._prepare_category_data(
            report.expense_by_category,
            report.total_expense,
            user_id
        )
        
        # Детальні дані категорій (з описами)
        data['income_data_detailed'] = self._prepare_detailed_category_data(
            report.incomes,
            report.total_income,
            user_id
        )
        
        data['expense_data_detailed'] = self._prepare_detailed_category_data(
            report.expenses,
            report.total_expense,
            user_id
        )
        
        # Транзакції
        data['transactions'] = self._prepare_transactions(report, user_id)
        
        # Денна динаміка
        daily_dynamics = self._prepare_daily_dynamics(report)
        
        # JSON дані для JavaScript (конвертуємо dict в list для збереження порядку)
        income_data_list = [{'key': k, **v} for k, v in data['income_data'].items()]
        expense_data_list = [{'key': k, **v} for k, v in data['expense_data'].items()]
        income_data_detailed_list = [{'key': k, **v} for k, v in data['income_data_detailed'].items()]
        expense_data_detailed_list = [{'key': k, **v} for k, v in data['expense_data_detailed'].items()]
        
        report_data_json = {
            'total_income': report.total_income,
            'total_expense': report.total_expense,
            'balance': report.net_balance,
            'income_count': report.income_count,
            'expense_count': report.expense_count,
            'total_transactions': report.transaction_count,
            'income_data': income_data_list,
            'expense_data': expense_data_list,
            'income_data_detailed': income_data_detailed_list,
            'expense_data_detailed': expense_data_detailed_list,
            'start_date': report.start_date,
            'end_date': report.end_date,
            'daily_dynamics': daily_dynamics,
        }
        data['report_data_json'] = json.dumps(report_data_json, ensure_ascii=False)
        
        return data
    
    def _get_interface_texts(self, user_id: int) -> Dict[str, str]:
        """Отримує всі тексти інтерфейсу."""
        return {
            'search_placeholder': get_text('search_placeholder', user_id=user_id),
            'income_title': get_text('report_total_income', user_id=user_id),
            'expense_title': get_text('report_total_expense', user_id=user_id),
            'balance_title': get_text('report_balance', user_id=user_id),
            'transactions_text': get_text('transactions_text', user_id=user_id),
            'positive_balance': get_text('positive_balance', user_id=user_id),
            'negative_balance': get_text('negative_balance', user_id=user_id),
            'overview_tab': get_text('overview_tab', user_id=user_id),
            'incomes_tab': get_text('incomes_tab', user_id=user_id),
            'expenses_tab': get_text('expenses_tab', user_id=user_id),
            'transactions_tab': get_text('transactions_tab', user_id=user_id),
            'overview_title': get_text('overview_title', user_id=user_id),
            'distribution_title': get_text('distribution_title', user_id=user_id),
            'income_categories': get_text('report_income_categories', user_id=user_id),
            'expense_categories': get_text('report_expense_categories', user_id=user_id),
            'no_income_data': get_text('no_income_data', user_id=user_id),
            'no_expense_data': get_text('no_expense_data', user_id=user_id),
            'all_transactions': get_text('all_transactions', user_id=user_id),
            'date_column': get_text('date_column', user_id=user_id),
            'type_column': get_text('type_column', user_id=user_id),
            'category_column': get_text('category_column', user_id=user_id),
            'description_column': get_text('description_column', user_id=user_id),
            'amount_column': get_text('amount_column', user_id=user_id),
            'income_badge': get_text('income_badge', user_id=user_id),
            'expense_badge': get_text('expense_badge', user_id=user_id),
            'no_transactions': get_text('no_transactions', user_id=user_id),
            'statistics_title': get_text('statistics_title', user_id=user_id),
            'generated_text': get_text('generated_text', user_id=user_id),
            'income_count_text': get_text('report_income_count', user_id=user_id),
            'expense_count_text': get_text('report_expense_count', user_id=user_id),
            'count_text': get_text('count_text', user_id=user_id),
            'simple_view_btn': get_text('simple_view_btn', user_id=user_id),
            'detailed_view_btn': get_text('detailed_view_btn', user_id=user_id),
            'dynamics_title': get_text('dynamics_title', user_id=user_id),
        }
    
    def _prepare_category_data(
        self,
        categories: Dict[str, float],
        total: float,
        user_id: int
    ) -> Dict[str, Dict]:
        """
        Підготовка даних категорій для відображення.
        Групує по основній категорії (без підкатегорій) і сортує по процентах.
        
        Args:
            categories: Словник категорій
            total: Загальна сума
            user_id: ID користувача
        
        Returns:
            dict: Підготовлені дані, відсортовані по процентах
        """
        # Групування по основній категорії (до двокрапки)
        grouped = {}
        
        for category_key, amount in categories.items():
            # Витягуємо основну категорію (до двокрапки)
            main_category = category_key.split(':')[0].strip() if ':' in category_key else category_key
            
            if main_category not in grouped:
                grouped[main_category] = 0
            grouped[main_category] += amount
        
        # Підготовка результату з процентами
        result = {}
        for category_name, amount in grouped.items():
            percentage = (amount / total * 100) if total > 0 else 0
            # Перекладаємо назву категорії з БД
            translated_name = translate_category_name(category_name, user_id=user_id)
            result[category_name] = {
                'name': translated_name,
                'amount': f"{amount:.2f}",
                'percent': f"{percentage:.2f}",
                'percent_value': percentage  # Для сортування
            }
        
        # Сортування по процентах (найбільші першими)
        result = dict(sorted(result.items(), key=lambda x: x[1]['percent_value'], reverse=True))
        
        return result
    
    def _prepare_detailed_category_data(
        self,
        transactions: List,
        total: float,
        user_id: int
    ) -> Dict[str, Dict]:
        """
        Підготовка детальних даних категорій (з описами транзакцій).
        
        Args:
            transactions: Список транзакцій (Income або Expense)
            total: Загальна сума
            user_id: ID користувача
        
        Returns:
            dict: Детальні дані з описами транзакцій, відсортовані по процентах
        """
        from database import CategoryRepository
        from collections import defaultdict
        
        # Групуємо транзакції по категоріях
        grouped = defaultdict(lambda: {'amount': 0.0, 'items': []})
        
        for transaction in transactions:
            # Отримуємо назву категорії
            category = CategoryRepository.get_category_by_id(transaction.category_id)
            category_name = category.name if category else get_text('unknown_category', user_id=user_id)
            
            # Перекладаємо назву категорії
            translated_category_name = translate_category_name(category_name, user_id=user_id)
            
            # Додаємо суму
            grouped[translated_category_name]['amount'] += transaction.amount
            
            # Додаємо опис транзакції (якщо є)
            if transaction.description:
                grouped[translated_category_name]['items'].append({
                    'description': transaction.description,
                    'amount': transaction.amount,
                    'add_date': transaction.add_date  # Повна дата з часом
                })
        
        # Підготовка результату з процентами та описами
        result = {}
        for category_name, data in grouped.items():
            percentage = (data['amount'] / total * 100) if total > 0 else 0
            result[category_name] = {
                'name': category_name,
                'amount': f"{data['amount']:.2f}",
                'percent': f"{percentage:.2f}",
                'percent_value': percentage,  # Для сортування
                'items': data['items']  # Список описів
            }
        
        # Сортування по процентах (найбільші першими)
        result = dict(sorted(result.items(), key=lambda x: x[1]['percent_value'], reverse=True))
        
        return result
    
    def _prepare_transactions(
        self,
        report: ReportData,
        user_id: int
    ) -> List[Dict]:
        """
        Підготовка списку транзакцій.
        
        Args:
            report: Дані звіту
            user_id: ID користувача
        
        Returns:
            list: Список транзакцій
        """
        transactions = []
        
        # Доходи
        for income in report.incomes:
            # Отримуємо назву категорії з бази
            from database import CategoryRepository
            category = CategoryRepository.get_category_by_id(income.category_id)
            category_name = category.name if category else get_text('unknown_category', user_id=user_id)
            
            # Перекладаємо назву категорії
            translated_category_name = translate_category_name(category_name, user_id=user_id)
            
            transactions.append({
                'date': income.add_date.split()[0] if ' ' in income.add_date else income.add_date,
                'type': 'income',
                'category': translated_category_name,
                'description': income.description if income.description else '',
                'amount': f"{income.amount:.2f}",
                'amount_value': income.amount  # Числове значення для сортування
            })
        
        # Витрати
        for expense in report.expenses:
            # Отримуємо назву категорії
            category = CategoryRepository.get_category_by_id(expense.category_id)
            category_name = category.name if category else get_text('unknown_category', user_id=user_id)
            
            # Перекладаємо назву категорії
            translated_category_name = translate_category_name(category_name, user_id=user_id)
            
            transactions.append({
                'date': expense.add_date.split()[0] if ' ' in expense.add_date else expense.add_date,
                'type': 'expense',
                'category': translated_category_name,
                'description': expense.description if expense.description else '',
                'amount': f"{expense.amount:.2f}",
                'amount_value': expense.amount  # Числове значення для сортування
            })
        
        # Сортування за сумою (найбільші зверху)
        transactions.sort(key=lambda x: x.get('amount_value', 0), reverse=True)
        
        return transactions
    
    def _prepare_daily_dynamics(self, report: ReportData) -> List[Dict]:
        """
        Підготовка денної динаміки доходів, витрат та балансу.
        
        Args:
            report: Дані звіту
        
        Returns:
            list: Список словників з даними по кожному дню
        """
        from collections import defaultdict
        from datetime import datetime
        
        # Збираємо дані по днях
        daily_data = defaultdict(lambda: {'income': 0.0, 'expense': 0.0})
        
        # Доходи по днях
        for income in report.incomes:
            date_str = income.add_date.split()[0] if ' ' in income.add_date else income.add_date
            daily_data[date_str]['income'] += income.amount
        
        # Витрати по днях
        for expense in report.expenses:
            date_str = expense.add_date.split()[0] if ' ' in expense.add_date else expense.add_date
            daily_data[date_str]['expense'] += expense.amount
        
        # Конвертуємо в список та сортуємо по даті
        result = []
        running_balance = 0.0
        
        for date_str in sorted(daily_data.keys()):
            data = daily_data[date_str]
            running_balance += data['income'] - data['expense']
            
            result.append({
                'date': date_str,
                'income': round(data['income'], 2),
                'expense': round(data['expense'], 2),
                'balance': round(running_balance, 2)
            })
        
        return result


def generate_html_report(
    report_data: ReportData,
    user_id: int,
    lang: str = 'uk'
) -> str:
    """
    Функція-обгортка для швидкої генерації HTML звіту.
    
    Args:
        report_data: Дані звіту
        user_id: ID користувача
        lang: Мова звіту
    
    Returns:
        str: Шлях до згенерованого файлу
    """
    generator = HTMLReportGenerator()
    return generator.generate_report(report_data, user_id, lang)
