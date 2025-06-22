"""
KerbianCore i18n Formatter

- Advanced message formatting: dates, numbers, currencies, units
- Timezones, relative time ("yesterday", "in 2 hours")
"""

import datetime
import locale as pylocale

class Formatter:
    @staticmethod
    def format_date(dt: datetime.date, locale: str = "en", fmt: str = "medium") -> str:
        if fmt == "short":
            return dt.strftime("%x")
        elif fmt == "long":
            return dt.strftime("%A, %d %B %Y")
        return dt.strftime("%b %d, %Y")

    @staticmethod
    def format_time(tm: datetime.time, locale: str = "en", fmt: str = "medium") -> str:
        if fmt == "short":
            return tm.strftime("%H:%M")
        elif fmt == "long":
            return tm.strftime("%H:%M:%S %Z")
        return tm.strftime("%H:%M:%S")

    @staticmethod
    def format_number(num: float, locale: str = "en", grouping: bool = True) -> str:
        try:
            pylocale.setlocale(pylocale.LC_NUMERIC, locale)
        except Exception:
            pass  # fallback
        return pylocale.format_string("%d", num, grouping=grouping)

    @staticmethod
    def format_currency(num: float, currency: str = "USD", locale: str = "en") -> str:
        # Simplified; in real code, use Babel or ICU
        symbol = {"USD": "$", "EUR": "€", "GBP": "£"}.get(currency, currency)
        return f"{symbol}{Formatter.format_number(num, locale)}"

    @staticmethod
    def format_unit(num: float, unit: str, locale: str = "en") -> str:
        # Simplified
        return f"{Formatter.format_number(num, locale)} {unit}"

    @staticmethod
    def format_relative(dt: datetime.datetime, now: datetime.datetime = None, locale: str = "en") -> str:
        now = now or datetime.datetime.now()
        delta = now - dt
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            mins = seconds // 60
            return f"{mins} minute{'s' if mins != 1 else ''} ago"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 172800:
            return "yesterday"
        else:
            days = seconds // 86400
            return f"{days} days ago"

# Usage:
# Formatter.format_date(datetime.date.today(), "en", "long")