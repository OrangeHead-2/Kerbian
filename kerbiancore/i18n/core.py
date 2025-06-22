"""
KerbianCore i18n Core

- Locale management and switching
- String lookup with fallback
- Interpolation (variables, HTML, etc.)
"""

import threading
from typing import Any, Dict, Callable, Optional
from kerbiancore.i18n.catalog import Catalog

class I18nManager:
    def __init__(self, catalogs: Dict[str, Catalog], default_locale='en', fallback_locales=None):
        self.catalogs = catalogs  # {locale: Catalog}
        self.default_locale = default_locale
        self.fallback_locales = fallback_locales or []
        self._local = threading.local()
        self._local.current_locale = default_locale

    def set_locale(self, locale: str):
        self._local.current_locale = locale

    def get_locale(self):
        return getattr(self._local, "current_locale", self.default_locale)

    def gettext(self, key: str, vars: Optional[Dict[str, Any]] = None, locale: Optional[str] = None, html: bool = False):
        locale = locale or self.get_locale()
        cat = self.catalogs.get(locale)
        if not cat:
            for fb in self.fallback_locales:
                cat = self.catalogs.get(fb)
                if cat:
                    break
            else:
                cat = self.catalogs[self.default_locale]
        val = cat.get(key)
        if val is None:
            val = key  # Fallback to key itself
        return self.interpolate(val, vars=vars, html=html)

    def interpolate(self, template: str, vars: Optional[Dict[str, Any]] = None, html: bool = False) -> str:
        if not vars:
            return template
        if html:
            # Optionally escape, or support HTML-safe formatting
            return template.format(**{k: self._html_escape(v) for k, v in vars.items()})
        return template.format(**vars)

    @staticmethod
    def _html_escape(s):
        import html
        if isinstance(s, str):
            return html.escape(s)
        return s

# Usage:
# i18n = I18nManager({"en": Catalog(...), "fr": Catalog(...)})
# i18n.set_locale("fr")
# i18n.gettext("hello_name", {"name": "Alice"})