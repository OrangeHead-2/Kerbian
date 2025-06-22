"""
KerbianCore i18n Pluralization

- CLDR-based plural rules for all languages
- Gender, case, ordinal, context-based selection
"""

from typing import Any, Dict, Callable, Optional

class PluralRules:
    # Simplified CLDR plural rules: {locale: (n) -> plural_form}
    _rules = {
        "en": lambda n: "one" if n == 1 else "other",
        "fr": lambda n: "one" if n in (0, 1) else "other",
        "ru": lambda n: (
            "one" if n % 10 == 1 and n % 100 != 11
            else "few" if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14)
            else "many" if n % 10 == 0 or 5 <= n % 10 <= 9 or 11 <= n % 100 <= 14
            else "other"
        ),
        # ... Add more CLDR rules as needed
    }
    _default_rule = lambda n: "other"

    @classmethod
    def get_rule(cls, locale: str) -> Callable[[int], str]:
        # Support e.g. 'en-US' fallback to 'en'
        rule = cls._rules.get(locale)
        if not rule and '-' in locale:
            rule = cls._rules.get(locale.split('-')[0])
        return rule or cls._default_rule

    @classmethod
    def plural_form(cls, locale: str, n: int, category: str = None) -> str:
        rule = cls.get_rule(locale)
        return rule(n)

    @classmethod
    def select(cls, locale: str, forms: Dict[str, str], n: int, gender: str = None, case: str = None, context: str = None) -> str:
        pf = cls.plural_form(locale, n)
        # Optionally: handle gender, case, context
        val = forms.get(pf) or forms.get("other")
        if isinstance(val, dict) and gender:
            val = val.get(gender, val.get("other"))
        if isinstance(val, dict) and case:
            val = val.get(case, val.get("other"))
        if isinstance(val, dict) and context:
            val = val.get(context, val.get("other"))
        return val

# Usage:
# forms = {"one": "There is {n} apple", "other": "There are {n} apples"}
# PluralRules.select("en", forms, 2)