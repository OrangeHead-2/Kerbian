"""
KerbianCore i18n Extraction/Scanner

- Extract translatable strings from Python, templates, JSON
- Catalog merge, deduplication, update
"""

import ast
import re
import json
from typing import List, Set, Dict, Callable

def extract_strings_from_python(source: str, funcnames: List[str] = ["_", "gettext"]) -> Set[str]:
    """Extracts strings from function calls (_("...")) in Python source."""
    found = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, 'id') and node.func.id in funcnames:
            if node.args and isinstance(node.args[0], ast.Str):
                found.add(node.args[0].s)
    return found

def extract_strings_from_template(source: str, regex=r"\{\{ *_\(['\"](.*?)['\"]\) *\}\}") -> Set[str]:
    """Extracts strings from template-style {{ _('string') }}."""
    return set(re.findall(regex, source))

def extract_strings_from_json(source: str, keys: List[str] = ["_t", "text"]) -> Set[str]:
    """Extracts strings from JSON fields that hold translatable content."""
    found = set()
    def scan(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in keys and isinstance(v, str):
                    found.add(v)
                else:
                    scan(v)
        elif isinstance(obj, list):
            for v in obj:
                scan(v)
    scan(json.loads(source))
    return found

def merge_catalogs(*catalogs: List[Dict[str, str]]) -> Dict[str, str]:
    merged = {}
    for cat in catalogs:
        merged.update(cat)
    return merged

def deduplicate(strings: List[str]) -> List[str]:
    return list(set(strings))

def update_catalog(old: Dict[str, str], new_strings: List[str]) -> Dict[str, str]:
    updated = {k: old.get(k, "") for k in new_strings}
    return updated

# Usage: See README for workflows