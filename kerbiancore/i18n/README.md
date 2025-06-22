# KerbianCore i18n — Internationalization & Pluralization

A robust Python internationalization engine with pluralization, gender, and context-aware selection.

---

## Features

- **Locale Management:** Runtime locale switching, per-thread, fallback
- **String Lookup:** Fast lookup, fallback to default, safe interpolation
- **Pluralization:** CLDR rules for all languages, gender/ordinal/context support
- **Extraction:** Scan code/templates/JSON for translatable strings, catalog update/merge/deduplication
- **Catalogs:** In-memory and on-disk catalogs, hot-reload, custom backend support
- **Formatting:** Dates, times, currencies, units, relative time, timezones
- **Extensible:** Add plurals, backends, extractors, formatters

---

## Quickstart

```python
from kerbiancore.i18n.core import I18nManager
from kerbiancore.i18n.catalog import Catalog

en = Catalog.from_file("en.json")
fr = Catalog.from_file("fr.json")
i18n = I18nManager({"en": en, "fr": fr}, default_locale="en", fallback_locales=["en"])

i18n.set_locale("fr")
print(i18n.gettext("welcome", {"name": "Alice"}))
```

---

## Pluralization

```python
from kerbiancore.i18n.plural import PluralRules

forms = {"one": "There is {n} apple", "other": "There are {n} apples"}
print(PluralRules.select("en", forms, 3, gender="male"))
```

---

## Extraction

```python
from kerbiancore.i18n.extract import extract_strings_from_python

with open("app.py") as f:
    print(extract_strings_from_python(f.read()))
```

---

## Catalogs

```python
from kerbiancore.i18n.catalog import Catalog

cat = Catalog.from_file("fr.json")
cat.set("hello", "Bonjour")
cat.save()
cat.reload()
```

---

## Formatting

```python
from kerbiancore.i18n.formatter import Formatter
from datetime import datetime

print(Formatter.format_date(datetime.now()))
print(Formatter.format_currency(1234.56, "USD"))
print(Formatter.format_relative(datetime.now(), datetime.now()))
```

---

## Workflow

1. Extract strings → update catalogs
2. Translate catalogs
3. Load catalogs at runtime
4. Switch locale as needed

---

## Best Practices

- Always use keys, not raw strings, for lookup.
- Use plural/gender/context forms for all user-facing strings.
- Keep catalogs in version control.
- Validate catalogs after extraction.
- Use tests to ensure all keys exist in all locales.

---