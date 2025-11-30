# -*- coding: utf-8 -*-
"""
Currency conversion utilities with caching and multiple sources.
Supports UAH, USD, EUR conversions.
"""

import requests
from datetime import datetime, timedelta
from threading import Lock
from typing import Dict, Optional
from locales.locale_manager import get_text

# Cache для курсів валют
_rate_cache: Dict[str, Dict] = {}
_cache_lock = Lock()
_cache_duration = timedelta(hours=1)

# Фіксовані курси як fallback (оновлено 2025-11-30)
FALLBACK_RATES = {
    'UAH': {
        'UAH': 1.0,
        'USD': 0.024,  # ~41.5 UAH за USD
        'EUR': 0.023,  # ~43.5 UAH за EUR
    },
    'USD': {
        'UAH': 41.5,
        'USD': 1.0,
        'EUR': 0.95,
    },
    'EUR': {
        'UAH': 43.5,
        'USD': 1.05,
        'EUR': 1.0,
    }
}


def _get_cached_rates() -> Optional[Dict[str, Dict]]:
    """Отримати курси з кешу, якщо вони не застаріли."""
    with _cache_lock:
        if _rate_cache.get('timestamp'):
            cache_time = _rate_cache['timestamp']
            if datetime.now() - cache_time < _cache_duration:
                return _rate_cache.get('rates')
    return None


def _set_cached_rates(rates: Dict[str, Dict]):
    """Зберегти курси в кеш."""
    with _cache_lock:
        _rate_cache['rates'] = rates
        _rate_cache['timestamp'] = datetime.now()


def _fetch_rates_from_nbu() -> Optional[Dict[str, Dict]]:
    """
    Отримати курси з API НБУ (Національний банк України).
    Повертає курси відносно UAH.
    """
    try:
        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            usd_rate = None
            eur_rate = None
            
            for item in data:
                if item['cc'] == 'USD':
                    usd_rate = float(item['rate'])
                elif item['cc'] == 'EUR':
                    eur_rate = float(item['rate'])
            
            if usd_rate and eur_rate:
                rates = {
                    'UAH': {
                        'UAH': 1.0,
                        'USD': 1.0 / usd_rate,
                        'EUR': 1.0 / eur_rate,
                    },
                    'USD': {
                        'UAH': usd_rate,
                        'USD': 1.0,
                        'EUR': usd_rate / eur_rate,
                    },
                    'EUR': {
                        'UAH': eur_rate,
                        'USD': eur_rate / usd_rate,
                        'EUR': 1.0,
                    }
                }
                return rates
    except Exception as e:
        print(f"[!] Error fetching rates from NBU: {e}")
    
    return None


def _fetch_rates_from_exchangerate_api() -> Optional[Dict[str, Dict]]:
    """
    Отримати курси з ExchangeRate-API.
    Безкоштовний сервіс для конвертації валют.
    """
    try:
        # Використовуємо USD як базову валюту
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            rates_usd = data.get('rates', {})
            
            uah_rate = rates_usd.get('UAH')
            eur_rate = rates_usd.get('EUR')
            
            if uah_rate and eur_rate:
                rates = {
                    'UAH': {
                        'UAH': 1.0,
                        'USD': 1.0 / uah_rate,
                        'EUR': eur_rate / uah_rate,
                    },
                    'USD': {
                        'UAH': uah_rate,
                        'USD': 1.0,
                        'EUR': eur_rate,
                    },
                    'EUR': {
                        'UAH': uah_rate / eur_rate,
                        'USD': 1.0 / eur_rate,
                        'EUR': 1.0,
                    }
                }
                return rates
    except Exception as e:
        print(f"[!] Error fetching rates from ExchangeRate-API: {e}")
    
    return None


def get_exchange_rates() -> Dict[str, Dict]:
    """
    Отримати актуальні курси валют з кешу або API.
    Спочатку перевіряє кеш, потім NBU, потім ExchangeRate-API,
    якщо всі джерела недоступні - повертає фіксовані курси.
    
    Returns:
        Dict з курсами у форматі: {'UAH': {'USD': rate, 'EUR': rate, ...}, ...}
    """
    # Спробувати отримати з кешу
    cached = _get_cached_rates()
    if cached:
        return cached
    
    # Спробувати отримати з НБУ
    rates = _fetch_rates_from_nbu()
    if rates:
        _set_cached_rates(rates)
        print("[OK] Exchange rates fetched from NBU")
        return rates
    
    # Спробувати отримати з ExchangeRate-API
    rates = _fetch_rates_from_exchangerate_api()
    if rates:
        _set_cached_rates(rates)
        print("[OK] Exchange rates fetched from ExchangeRate-API")
        return rates
    
    # Використати фіксовані курси
    print("[!] Using fallback exchange rates")
    return FALLBACK_RATES


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Конвертувати суму з однієї валюти в іншу.
    
    Args:
        amount: Сума для конвертації
        from_currency: Валюта джерела ('UAH', 'USD', 'EUR')
        to_currency: Цільова валюта ('UAH', 'USD', 'EUR')
    
    Returns:
        Сконвертована сума
    
    Example:
        >>> convert_currency(100, 'USD', 'UAH')
        4150.0
    """
    if from_currency == to_currency:
        return amount
    
    rates = get_exchange_rates()
    
    try:
        rate = rates[from_currency][to_currency]
        return round(amount * rate, 2)
    except KeyError:
        print(f"[!] Currency conversion error: {from_currency} -> {to_currency}")
        return amount


def get_currency_symbol(currency: str) -> str:
    """
    Отримати символ валюти.
    
    Args:
        currency: Код валюти ('UAH', 'USD', 'EUR')
    
    Returns:
        Символ валюти
    """
    symbols = {
        'UAH': '₴',
        'USD': '$',
        'EUR': '€',
    }
    return symbols.get(currency, currency)


def format_amount_with_currency(amount: float, currency: str) -> str:
    """
    Форматувати суму з символом валюти.
    
    Args:
        amount: Сума
        currency: Валюта
    
    Returns:
        Відформатована строка (наприклад, "100.50 ₴")
    """
    symbol = get_currency_symbol(currency)
    return f"{amount:.2f} {symbol}"


def get_rate_info(user_id: int = None) -> str:
    """
    Отримати інформацію про поточні курси валют у текстовому вигляді.
    
    Args:
        user_id: ID користувача для локалізації
    
    Returns:
        Текст з курсами валют
    """
    rates = get_exchange_rates()
    
    text = get_text('currency_rates_title', user_id=user_id) + "\n\n"
    
    # USD -> UAH, EUR
    text += f"1 USD = {rates['USD']['UAH']:.2f} UAH\n"
    text += f"1 USD = {rates['USD']['EUR']:.4f} EUR\n\n"
    
    # EUR -> UAH, USD
    text += f"1 EUR = {rates['EUR']['UAH']:.2f} UAH\n"
    text += f"1 EUR = {rates['EUR']['USD']:.4f} USD\n\n"
    
    # UAH -> USD, EUR
    text += f"1 UAH = {rates['UAH']['USD']:.4f} USD\n"
    text += f"1 UAH = {rates['UAH']['EUR']:.4f} EUR\n"
    
    # Додати інформацію про оновлення
    if _rate_cache.get('timestamp'):
        update_time = _rate_cache['timestamp'].strftime('%H:%M')
        text += "\n" + get_text('updated_at', user_id=user_id).format(update_time)
    
    return text


# Тестування при запуску модуля
if __name__ == '__main__':
    print("Testing currency converter...")
    
    rates = get_exchange_rates()
    print("\nCurrent rates:")
    for from_curr, to_rates in rates.items():
        print(f"\n{from_curr}:")
        for to_curr, rate in to_rates.items():
            print(f"  -> {to_curr}: {rate:.4f}")
    
    print("\nConversion examples:")
    print(f"100 USD -> UAH: {convert_currency(100, 'USD', 'UAH')}")
    print(f"1000 UAH -> USD: {convert_currency(1000, 'UAH', 'USD')}")
    print(f"100 EUR -> UAH: {convert_currency(100, 'EUR', 'UAH')}")
    
    print("\nRate info:")
    print(get_rate_info())
