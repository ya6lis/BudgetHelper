# -*- coding: utf-8 -*-
"""
English localization for Budget Helper.
"""

TEXTS_EN = {
    # General
    'welcome': '👋 Welcome to Budget Helper!\n\n📊 Your personal budget management assistant\n\n✨ What you can do:\n• 💰 Track income\n• 💸 Control expenses\n• 📈 View statistics\n• 📊 Analyze budget\n\nSelect an option below to get started:',
    'main_menu_info': '🏠 Main Menu\n\n💡 Here you can manage your finances:\n• View income and expense statistics\n• Add new records\n• Analyze your budget\n\nSelect an option:',
    'back_to_main': '🔙 Returning to main menu:',
    'feature_not_ready': '⚠️ This feature is not yet implemented. Please wait for updates.',
    
    # Menu buttons
    'menu_my_finances': '📊 My Finances',
    'menu_add_expense': '➕ Add New Expense',
    'menu_add_income': '➕ Add New Income',
    'menu_report': '📈 Report / Budget Analysis',
    'menu_settings': '⚙️ Settings',
    'menu_back': '⬅️ Back',
    'menu_main': '🏠 Main Menu',
    'menu_view_expenses': '💸 View Expenses',
    'menu_view_incomes': '💰 View Incomes',
    'menu_view_general_finances': '📊 View General Finances',
    'menu_another_period': '📅 Another Period',
    
    # Time periods
    'period_today': '📅 Today',
    'period_week': '📅 This Week',
    'period_month': '📅 This Month',
    'period_year': '📅 This Year',
    
    # Incomes
    'income_select_type': '💰 Adding Income\n\n📋 Select the category your income belongs to:\n\n💡 This will help you better analyze income sources.',
    'income_enter_amount': '💵 Enter income amount for category "{}":\n\n📝 Example: 5000 or 5000.50 or 5000,50',
    'income_added': '✅ Income added: {} UAH — {}\n\n💡 Now you can:\n• Add another income\n• View statistics in "My Finances"',
    'income_invalid_amount': '⚠️ Invalid amount!\n\n✅ Correct: 100, 250.50, 250,50\n❌ Incorrect: 0, -100, nan, inf\n\n📌 Requirements:\n• Numbers only (dot or comma)\n• Greater than 0.01 UAH\n• Less than 1,000,000,000 UAH\n\nTry again or go back.',
    'income_type_salary': 'Salary',
    'income_type_bonus': 'Bonus',
    'income_type_gift': 'Gift',
    'income_type_other': 'Other',
    
    # View incomes
    'view_incomes_select_period': '💰 View Incomes\n\n📅 Select the period for which you want to see detailed information about your income:\n\n💡 You will see all income records and their categories.',
    'view_incomes_invalid_choice': 'Invalid choice, please select from the menu.',
    'view_incomes_period_error': 'Error in period selection. Try again.',
    'view_incomes_no_data': '💡 Unfortunately, there are no incomes for the selected period.\n\n📝 Add your first income through the main menu!',
    'view_incomes_title': "📈 Incomes for period '{}':\n\n",
    'view_incomes_total': '\n🔹 Total income: {:.2f} UAH',
    'view_incomes_select_another': 'Select period to view incomes:',
    
    # Expenses
    'expense_select_type': '💸 Adding Expense\n\n📋 Select the category your expense belongs to:\n\n💡 This will help you track where your money goes.',
    'expense_enter_amount': '💵 Enter expense amount for category "{}":\n\n📝 Example: 150 or 150.75 or 150,75',
    'expense_added': '✅ Expense added: {} UAH — {}\n\n💡 Now you can:\n• Add another expense\n• View statistics in "My Finances"',
    'expense_invalid_amount': '⚠️ Invalid amount!\n\n✅ Correct: 50, 125.99, 125,99\n❌ Incorrect: 0, -50, nan, inf\n\n📌 Requirements:\n• Numbers only (dot or comma)\n• Greater than 0.01 UAH\n• Less than 1,000,000,000 UAH\n\nTry again or go back.',
    
    # View expenses
    'view_expenses_select_period': '💸 View Expenses\n\n📅 Select the period for which you want to see detailed information about your expenses:\n\n💡 You will see all expenses grouped by categories.',
    'view_expenses_invalid_choice': 'Invalid choice, please select from the menu.',
    'view_expenses_period_error': 'Error in period selection. Try again.',
    'view_expenses_no_data': '💡 Unfortunately, there are no expenses for the selected period.\n\n📝 Add your first expense through the main menu!',
    'view_expenses_title': "💸 Expenses for period '{}':\n\n",
    'view_expenses_total': '\n🔹 Total expenses: {:.2f} UAH',
    'view_expenses_select_another': 'Select period to view expenses:',
    
    # Finances
    'finance_select_option': 'Please select what you want to view 📊:',
    'finance_menu_info': '📊 My Finances\n\n💰 Incomes - view all income records\n💸 Expenses - detailed expense information\n📈 General statistics - balance and analysis\n\nSelect a section:',
    
    # General finances
    'view_general_select_period': '📊 General Finances\n\n📅 Select a period to view your balance:\n\n💡 You will see income, expenses, and balance for the selected period.',
    'view_general_no_data': '💡 Unfortunately, there are no financial transactions for the selected period.\n\n📝 Add income or expenses through the main menu!',
    'view_general_title': "📊 General Finances '{}'\n\n",
    'view_general_income': '💰 Income: {:.2f} UAH',
    'view_general_expense': '💸 Expenses: {:.2f} UAH',
    'view_general_balance_positive': '\n📈 Balance: +{:.2f} UAH\n\n✅ Your finances are positive!',
    'view_general_balance_negative': '\n📉 Balance: {:.2f} UAH\n\n⚠️ Expenses exceed income.',
    'view_general_balance_zero': '\n⚖️ Balance: 0.00 UAH\n\n💡 Income and expenses are balanced.',
    'view_general_select_another': 'Select period to view general finances:',
    
    # Settings
    'settings_menu': '⚙️ Settings\n\n🛠 Here you can:\n• Change interface language\n• Configure parameters (coming soon)\n• Manage categories (coming soon)\n\nSelect an option:',
    'settings_change_language': '🌐 Change Language',
    'settings_select_language': '🌐 Select interface language:\n\n🇺🇦 Українська\n🇬🇧 English\n\nThe selected language will be applied to all menus and messages.',
    'settings_language_changed': '✅ Language changed successfully!\n\n💡 Now the entire interface will be displayed in the selected language.',
    'settings_invalid_language': '❌ Invalid language choice. Try again.',
}
