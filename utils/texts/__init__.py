"""All the texts of the app, in English (official) and French. One module per page, merged here."""
from importlib import import_module

MODULES = ["common", "report", "home", "reading", "town", "compare", "mapview", "monitor", "quality",
           "conclusions", "about"]

TEXTS: dict[str, dict[str, str]] = {}
for _name in MODULES:
    _part = import_module(f"utils.texts.{_name}").T
    _dup = set(_part) & set(TEXTS)
    if _dup:
        raise KeyError(f"duplicated text keys in utils/texts/{_name}.py: {sorted(_dup)}")
    TEXTS.update(_part)
