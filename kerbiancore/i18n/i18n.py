import threading
import re
import json

class KerbianI18n:
    def __init__(self, default_lang="en"):
        self.translations = {}  # lang -> { key: str|dict }
        self.lock = threading.Lock()
        self.default_lang = default_lang
        self.plural_rules = {
            "en": lambda n: "one" if n == 1 else "other",
            "fr": lambda n: "one" if n in (0, 1) else "other",
            "ru": lambda n: "one" if n%10==1 and n%100!=11 else "few" if 2<=n%10<=4 and (n%100<10 or n%100>=20) else "many" if n%10==0 or 5<=n%10<=9 or 11<=n%100<=14 else "other",
        }
        self.param_pattern = re.compile(r"\{(\w+)\}")

    def add_translation(self, lang, key, value):
        with self.lock:
            if lang not in self.translations:
                self.translations[lang] = {}
            self.translations[lang][key] = value

    def translate(self, key, lang=None, count=None, fallback=None, **kwargs):
        lang = lang or self.default_lang
        with self.lock:
            d = self.translations.get(lang, {})
            val = d.get(key)
            if val is None and fallback:
                val = fallback
            elif val is None:
                val = self.translations.get(self.default_lang, {}).get(key, key)
        template = val
        # Pluralization
        if isinstance(val, dict) and count is not None:
            form = self._plural_form(lang, count)
            template = val.get(form) or val.get("other") or next(iter(val.values()))
        # String interpolation
        if isinstance(template, str):
            params = {"count": count} if count is not None else {}
            params.update(kwargs)
            return self.param_pattern.sub(lambda m: str(params.get(m.group(1), m.group(0))), template)
        return str(template)

    def _plural_form(self, lang, count):
        rule = self.plural_rules.get(lang)
        if rule:
            return rule(count)
        return "other"

    def available_languages(self):
        with self.lock:
            return list(self.translations.keys())

    def keys_for_language(self, lang=None):
        lang = lang or self.default_lang
        with self.lock:
            return list(self.translations.get(lang, {}).keys())

    def remove_translation(self, lang, key):
        with self.lock:
            self.translations.get(lang, {}).pop(key, None)

    def export_translations(self, lang=None):
        lang = lang or self.default_lang
        with self.lock:
            return dict(self.translations.get(lang, {}))

    def import_translations(self, lang, data):
        with self.lock:
            self.translations[lang] = dict(data)

    def save_to_file(self, path):
        with self.lock:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.translations, f, ensure_ascii=False, indent=2)

    def load_from_file(self, path):
        with self.lock:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)

    def merge_translations(self, lang, new_data):
        with self.lock:
            self.translations.setdefault(lang, {}).update(new_data)