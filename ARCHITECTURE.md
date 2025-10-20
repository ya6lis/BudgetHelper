# Архітектура проекту Budget Helper

## 🏗️ Загальна архітектура

```
┌─────────────────────────────────────────────────────────┐
│                   Telegram User                         │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                   main.py (Entry Point)                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  1. init_db()                                   │   │
│  │  2. init_bot()                                  │   │
│  │  3. bot.infinity_polling()                      │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
┌──────────────┐        ┌──────────────────┐
│  database/   │        │  bot/            │
│  init_db()   │        │  bot_instance.py │
└──────────────┘        └───────┬──────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐   ┌──────────┐
        │handlers/ │    │keyboards/│   │locales/  │
        └──────────┘    └──────────┘   └──────────┘
                │
        ┌───────┼───────┬─────────┬─────────┐
        ▼       ▼       ▼         ▼         ▼
    start.py income.py finance.py misc.py  ...
```

## 📦 Модулі та їх відповідальність

### 1. main.py
**Відповідальність:** Точка входу в додаток
- Ініціалізація БД
- Ініціалізація бота
- Запуск infinity polling

### 2. config/
**Відповідальність:** Конфігурація та константи проекту
```python
config/
├── __init__.py
├── config.py              # Завантаження змінних з .env
├── constants.py           # Константи (типи доходів/витрат, періоди)
└── callbacks.py           # Константи callback_data для навігації
```

**callbacks.py** - Централізовані callback константи:
- Головне меню (CALLBACK_MY_FINANCES, CALLBACK_ADD_INCOME, тощо)
- Контекстна навігація (CALLBACK_BACK_TO_FINANCES, CALLBACK_BACK_TO_VIEW_EXPENSES, тощо)
- Періоди часу (CALLBACK_PERIOD_TODAY, CALLBACK_PERIOD_WEEK, тощо)
- Типи операцій (INCOME_TYPE_CALLBACKS, EXPENSE_TYPE_CALLBACKS)
- Налаштування (CALLBACK_SETTINGS_LANGUAGE, CALLBACK_LANGUAGE_UK, тощо)

### 3. bot/
**Відповідальність:** Конфігурація та ініціалізація бота
```python
bot/
├── __init__.py           # Експорт bot та init_bot
└── bot_instance.py       # Створення TeleBot + реєстрація handlers
```

**Потік роботи:**
1. Створення екземпляра TeleBot з TOKEN
2. Імпорт всіх handlers
3. Реєстрація всіх handlers через register_handlers(bot)

### 4. database/
**Відповідальність:** Робота з базою даних (Repository Pattern + Models)
```python
database/
├── __init__.py              # Експорт всіх функцій
├── db_manager.py            # Менеджер БД
│   ├── get_connection()     # З'єднання з БД
│   ├── init_db()            # Створення таблиць
│   └── ensure_user()        # Перевірка користувача
├── user_repository.py       # Репозиторій користувачів
│   ├── get_user()           # Отримати користувача
│   ├── create_user()        # Створити користувача
│   ├── update_user_language() # Оновити мову
│   └── ensure_user_exists() # Перевірка/створення
├── income_repository.py     # Репозиторій доходів
│   ├── add_income()         # Додати дохід (повертає Income)
│   ├── get_income_by_id()   # Отримати дохід за ID
│   ├── get_all_incomes()    # Всі доходи (List[Income])
│   ├── get_incomes_aggregated() # Агреговані доходи
│   ├── update_income()      # Оновити дохід
│   └── delete_income()      # Видалити дохід
├── expense_repository.py    # Репозиторій витрат
│   ├── add_expense()        # Додати витрату (повертає Expense)
│   ├── get_expense_by_id()  # Отримати витрату за ID
│   ├── get_all_expenses()   # Всі витрати (List[Expense])
│   ├── get_expenses_aggregated() # Агреговані витрати
│   ├── update_expense()     # Оновити витрату
│   └── delete_expense()     # Видалити витрату
└── utils.py                 # Допоміжні функції
    └── get_date_range_for_period()  # Діапазони дат
```

**Паттерн:** Repository Pattern з Models
- Кожна таблиця має свій repository
- Repository працює з моделями (User, Income, Expense)
- Repository повертає моделі замість словників
- Інкапсулює всю логіку роботи з БД
- Легко тестувати та замінити БД

### 5. handlers/
**Відповідальність:** Обробка повідомлень від користувача
```python
handlers/
├── __init__.py          # Експорт всіх handlers
├── start.py             # /start, /help
├── income.py            # Додавання доходів + контекстна навігація
├── expenses.py          # Додавання витрат + контекстна навігація
├── finance.py           # Перегляд фінансів + back handlers
├── report.py            # Звіти та аналітика
├── settings.py          # Налаштування + контекстна навігація
└── misc.py              # Інші функції
```

**Структура handler:**
```python
def register_handlers(bot):
    """Реєстрація обробників."""
    
    @bot.message_handler(...)
    def handler_function(message):
        """Обробка повідомлення."""
        # Логіка обробки
    
    @bot.callback_query_handler(func=lambda call: call.data == 'CALLBACK_BACK_TO_...')
    def back_handler(call):
        """Контекстна навігація назад."""
        # Повернення до попереднього меню
```

**Контекстна навігація:**
- Кожен handler містить back_to_* функції для повернення до попереднього меню
- Використовує callback константи з config/callbacks.py
- Підтримує ієрархічну навігацію (Головне меню → Фінанси → Перегляд витрат → Період)

### 6. keyboards/
**Відповідальність:** Створення клавіатур
```python
keyboards/
├── __init__.py              # Експорт всіх клавіатур
└── main_keyboards.py        # Основні клавіатури
    ├── main_menu()          # Головне меню
    ├── finance_submenu()    # Підменю фінансів
    ├── back_button()        # Контекстна кнопка назад + головне меню
    ├── create_timeframe_keyboard()    # Вибір періоду з back_callback
    ├── create_income_types_keyboard() # Типи доходів з back_callback
    ├── create_expense_types_keyboard() # Типи витрат з back_callback
    ├── create_language_keyboard()     # Вибір мови з back_callback
    └── create_settings_keyboard()     # Меню налаштувань
```

**Функції клавіатур з параметром back_callback:**
- Кожна клавіатура приймає back_callback для контекстної навігації
- Якщо back_callback != CALLBACK_BACK_TO_MAIN, показуються дві кнопки:
  - "🏠 Головне меню" (CALLBACK_BACK_TO_MAIN)
  - "🔙 Назад" (back_callback)
- Обидві кнопки розташовані в окремому рядку внизу клавіатури

**Переваги централізації:**
- Уникнення дублювання коду
- Легко змінювати дизайн клавіатур
- Зручно підтримувати
- Контекстна навігація з підтримкою back_callback
- Подвійна навігація (Головне меню + Назад) для кращого UX

### 7. locales/
**Відповідальність:** Локалізація (переклади)
```python
locales/
├── __init__.py              # Експорт функцій локалізації
├── locale_manager.py        # Менеджер локалізації
│   ├── get_text()           # Отримати текст
│   ├── set_language()       # Встановити мову
│   ├── get_income_types()   # Типи доходів
│   ├── get_expense_types()  # Типи витрат
│   └── get_time_frames()    # Періоди часу
├── uk.py                    # Українська мова
└── en.py                    # Англійська мова
```

**Як працює:**
1. Кожна мова - окремий файл з словником
2. locale_manager керує доступом до текстів
3. get_text(key, user_id) повертає текст для мови користувача
4. Підтримка 'menu_main' та 'menu_back' для навігації

### 8. models/
**Відповідальність:** Моделі даних для представлення об'єктів
```python
models/
├── __init__.py              # Експорт всіх моделей
├── user.py                  # Модель користувача
├── income.py                # Модель доходу
└── expense.py               # Модель витрати
```

**Структура моделей:**
- Використовуються dataclasses для зручності
- Методи to_dict() та from_dict() для конвертації
- Валідація даних на рівні моделі
- Бізнес-логіка інкапсульована в моделях

**Приклад:**
```python
@dataclass
class Income:
    user_id: int
    amount: float
    description: str
    currency: str = 'UAH'
    add_date: Optional[str] = None
    update_date: Optional[str] = None
    id: Optional[int] = None
```

### 9. utils/
**Відповідальність:** Допоміжні функції
```python
utils/
├── __init__.py              # Експорт утиліт
├── formatters.py            # Форматування даних
├── message_helpers.py       # Допоміжні функції для повідомлень
└── validation.py            # Валідація вводу користувача
```

## 🔄 Потік даних

### Приклад: Додавання доходу

```
1. Користувач натискає "➕ Записати новий дохід"
   │
   ▼
2. handlers/income.py: income_start()
   │ - Отримує типи доходів з locales (get_income_types())
   │ - Створює клавіатуру з keyboards (create_income_types_keyboard)
   │ - Передає back_callback=CALLBACK_BACK_TO_MAIN
   │ - Відправляє повідомлення користувачу
   ▼
3. Користувач обирає тип доходу
   │
   ▼
4. handlers/income.py: income_type_selected()
   │ - Зберігає тип в user_states
   │ - Запитує суму через get_text('income_enter_amount')
   │ - Показує клавіатуру з back_callback=CALLBACK_BACK_TO_ADD_INCOME
   ▼
5. Користувач вводить суму
   │
   ▼
6. handlers/income.py: process_income_amount()
   │ - Валідує суму через validate_amount()
   │ - Викликає database.add_income(user_id, amount, description)
   ▼
7. database/income_repository.py: add_income()
   │ - Створює об'єкт Income (модель)
   │ - Зберігає в БД
   │ - Повертає Income з ID
   ▼
8. handlers/income.py:
   │ - Форматує успішне повідомлення через get_text()
   │ - Використовує дані з моделі Income (income.amount, income.description)
   │ - Відправляє підтвердження з main_menu()
   ▼
9. Користувач бачить підтвердження з головним меню

### Приклад: Контекстна навігація

```
1. Користувач: Головне меню → "💰 Мої фінанси"
   ▼
2. finance_submenu() показує підменю з кнопкою "Назад" → Головне меню
   ▼
3. Користувач: "👁️ Переглянути витрати"
   ▼
4. create_timeframe_keyboard(back_callback=CALLBACK_BACK_TO_FINANCES)
   │ - Показує періоди + двійні кнопки:
   │   ["🏠 Головне меню" | "🔙 Назад"]
   ▼
5. Користувач натискає "🔙 Назад"
   ▼
6. handlers/finance.py: back_to_finances()
   │ - Повертає до finance_submenu()
   │ - Не до головного меню!
   ▼
7. Користувач бачить підменю фінансів
```

## 🎯 Принципи дизайну

### 1. Separation of Concerns (Розділення відповідальності)
- Кожен модуль має свою чітку відповідальність
- Handlers - обробка повідомлень
- Database - робота з даними
- Keyboards - створення UI
- Locales - переклади
- Callbacks - константи навігації

### 2. DRY (Don't Repeat Yourself)
- Спільний код винесено в утиліти
- Клавіатури централізовані з параметром back_callback
- Тексти в одному місці (locales)
- Callback константи централізовані (config/callbacks.py)

### 3. Single Responsibility Principle
- Кожна функція робить одну річ
- Легко тестувати
- Легко підтримувати

### 4. Easy to Extend
- Додати нову мову - новий файл в locales/
- Додати новий handler - новий файл в handlers/
- Додати нову клавіатуру - нова функція в keyboards/

## 📈 Масштабування

### Додавання нової функції:

1. **Створити handler:**
   ```python
   # handlers/new_feature.py
   def register_handlers(bot):
       @bot.message_handler(...)
       def new_feature_handler(message):
           pass
   ```

2. **Зареєструвати в bot_instance.py:**
   ```python
   from handlers import new_feature
   new_feature.register_handlers(bot)
   ```

3. **Додати тексти в locales:**
   ```python
   # locales/uk.py
   'new_feature_text': 'Новий текст'
   ```

4. **Додати клавіатуру (якщо потрібно):**
   ```python
   # keyboards/main_keyboards.py
   def new_feature_keyboard():
       # ...
   ```

### Додавання нової мови:

1. **Створити файл:**
   ```python
   # locales/de.py
   TEXTS_DE = { ... }
   ```

2. **Зареєструвати в locale_manager.py:**
   ```python
   from .de import TEXTS_DE
   LANGUAGES = { 'uk': TEXTS_UK, 'en': TEXTS_EN, 'de': TEXTS_DE }
   ```

## 🔐 Безпека

- `.env` файл в `.gitignore`
- Токени не в коді
- SQL injection захист (prepared statements)
- Валідація користувацького вводу

## 📊 Майбутні покращення

1. **Логування:**
   - Додати модуль logging
   - Логувати всі операції

2. **Тести:**
   - Unit tests для handlers
   - Integration tests для БД

3. **Кешування:**
   - Redis для сесій
   - Кеш для часто використовуваних даних

4. **Аналітика:**
   - Графіки витрат/доходів
   - Прогнозування

5. **Нотифікації:**
   - Нагадування про бюджет
   - Щоденні/тижневі звіти
