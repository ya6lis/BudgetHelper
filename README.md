# Budget Helper Bot

Telegram бот для управління особистими фінансами.

## 📁 Структура проекту

```
BudgetHelper/
│
├── config/                   # Конфігурація проєкту
│   ├── __init__.py
│   ├── config.py             # Завантаження змінних оточення
│   └── constants.py          # Константи проєкту
│
├── bot/                      # Конфігурація бота
│   ├── __init__.py
│   └── bot_instance.py       # Екземпляр бота та ініціалізація
│
├── database/                 # Робота з базою даних
│   ├── __init__.py
│   ├── db_manager.py         # Менеджер БД та ініціалізація
│   ├── income_repository.py  # Репозиторій для доходів
│   └── utils.py              # Допоміжні функції для БД
│
├── handlers/                 # Обробники повідомлень
│   ├── __init__.py
│   ├── start.py              # Обробник /start
│   ├── income.py             # Обробник доходів
│   ├── expenses.py           # Обробник витрат (TODO)
│   ├── finance.py            # Обробник перегляду фінансів
│   ├── report.py             # Звіти (TODO)
│   ├── settings.py           # Налаштування (TODO)
│   └── misc.py               # Різні обробники
│
├── keyboards/                # Клавіатури бота
│   ├── __init__.py
│   └── main_keyboards.py     # Основні клавіатури
│
├── locales/                  # Локалізація (переклади)
│   ├── __init__.py
│   ├── locale_manager.py     # Менеджер локалізації
│   ├── uk.py                 # Українська мова
│   └── en.py                 # Англійська мова
│
├── utils/                    # Утиліти
│   ├── __init__.py
│   ├── message_helpers.py    # Хелпери для повідомлень
│   ├── validation.py         # Валідація даних
│   └── formatters.py         # Форматування фінансів
│
├── models/                   # Моделі даних (placeholder)
│   └── __init__.py
│
├── main.py                   # Точка входу в програму
├── config.py                 # Конфігураційні константи
├── texts.py                  # Текстові константи
├── .env                      # Змінні оточення (НЕ комітити!)
├── .env.example              # Приклад .env файлу
├── .gitignore                # Git ignore
├── requirements.txt          # Python залежності
├── README.md                 # Цей файл
├── QUICKSTART.md             # Швидкий старт
└── LICENSE                   # Ліцензія

```

## 🚀 Початок роботи

### Передумови

- Python 3.8+
- pip

### Встановлення

1. Клонуйте репозиторій:

```bash
git clone <your-repo-url>
cd BudgetHelper
```

2. Створіть віртуальне середовище:

```bash
python -m venv venv
```

3. Активуйте віртуальне середовище:

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Встановіть залежності:

```bash
pip install -r requirements.txt
```

5. Створіть `.env` файл на основі `.env.example`:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

6. Додайте ваш Telegram Bot Token в `.env`:

```
TELEGRAM_TOKEN=your_actual_bot_token_here
```

### Запуск бота

```bash
python main.py
```

## 📚 Архітектура

### Модулі

#### 1. **config/** - Конфігурація

- `config.py` - Завантаження змінних оточення (TOKEN)
- `constants.py` - Константи проекту (типи доходів/витрат, мови)

#### 2. **bot/** - Ініціалізація бота

- `bot_instance.py` - Створення екземпляра TeleBot та реєстрація всіх обробників

#### 3. **database/** - Робота з БД

- `db_manager.py` - З'єднання та ініціалізація таблиць
- `income_repository.py` - CRUD операції для доходів
- `utils.py` - Допоміжні функції (дати, періоди)

#### 4. **handlers/** - Обробники команд

Кожен handler відповідає за свою область функціональності:

- `start.py` - Команда /start
- `income.py` - Додавання доходів
- `expenses.py` - Додавання витрат (в розробці)
- `finance.py` - Перегляд фінансів (доходи за період)
- `report.py` - Звіти (в розробці)
- `settings.py` - Налаштування (в розробці)
- `misc.py` - Інші обробники

#### 5. **keyboards/** - Клавіатури

- `main_keyboards.py` - Всі клавіатури бота (головне меню, періоди, тощо)

#### 6. **locales/** - Локалізація

- `locale_manager.py` - Менеджер мов та отримання текстів
- `uk.py` - Українська мова (за замовчуванням)
- `en.py` - Англійська мова
- Підтримка багатомовності

#### 7. **utils/** - Допоміжні функції

- `message_helpers.py` - Відправка повідомлень з клавіатурами
- `validation.py` - Валідація даних (суми, команди)
- `formatters.py` - Форматування списків доходів/витрат

## 🔧 Додавання нових функцій

### Додавання нового обробника

1. Створіть файл в `handlers/`, наприклад `new_feature.py`
2. Реалізуйте функцію `register_handlers(bot)`:

```python
def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == 'Кнопка')
    def handle_button(message):
        bot.send_message(message.chat.id, 'Відповідь')
```

3. Додайте імпорт та реєстрацію в `bot/bot_instance.py`:

```python
from handlers import new_feature
new_feature.register_handlers(bot)
```

### Додавання нової мови

1. Створіть файл в `locales/`, наприклад `de.py`
2. Додайте словник перекладів `TEXTS_DE` (скопіюйте структуру з `uk.py`)
3. Зареєструйте мову в `locales/locale_manager.py`:

```python
LANGUAGES = {
    'uk': TEXTS_UK,
    'en': TEXTS_EN,
    'de': TEXTS_DE,  # новий
}
```

### Додавання нового типу доходу/витрати

1. Відкрийте `config/constants.py`
2. Додайте новий тип у відповідний словник:

```python
INCOME_TYPES = {
    'uk': ['Зарплата', 'Премія', 'Подарунок', 'Інвестиції', 'Інші'],
    #                                          ^^^^^^^^^^^ новий
}
```

## ✨ Поточний функціонал

### Реалізовано

- ✅ Додавання доходів з різними типами
- ✅ Перегляд доходів за період (сьогодні, тиждень, місяць, рік)
- ✅ Підтримка української та англійської мов
- ✅ База даних SQLite з Repository Pattern
- ✅ Модульна архітектура

### В розробці

- 🚧 Додавання витрат
- 🚧 Звіти та аналітика
- 🚧 Налаштування користувача
- 🚧 Експорт даних

## 📄 Ліцензія

Дивіться файл [LICENSE](LICENSE)
