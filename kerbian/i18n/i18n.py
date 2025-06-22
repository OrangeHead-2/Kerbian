import json, os

class I18n:
    def __init__(self, locale_dir, default='en'):
        self.translations = {}
        self.current = default
        self.load(locale_dir)

    def load(self, locale_dir):
        for fname in os.listdir(locale_dir):
            if fname.endswith('.json'):
                with open(os.path.join(locale_dir, fname), 'r') as f:
                    lang = fname.split('.')[0]
                    self.translations[lang] = json.load(f)

    def set_locale(self, lang):
        self.current = lang

    def t(self, key):
        return self.translations.get(self.current, {}).get(key, key)