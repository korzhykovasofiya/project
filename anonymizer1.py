import json
from patterns import PATTERNS, normalize
from filemanager import read_file, FileError

JOURNAL_PATH = "journal.json"


def find_data(text: str) -> list[tuple[int, int, str, str]]:
    matches = []
    for priority, (category, regexes) in enumerate(PATTERNS.items()):
        if not isinstance(regexes, list):
            regexes = [regexes]
        for regex in regexes:
            for m in regex.finditer(text):
                matches.append(
                    (m.start(), -len(m.group()), priority, m.end(), category, m.group())
                )  
    matches.sort()

    found = []
    last_end = 0
    for start, _, _, end, category, data in matches:
        if start >= last_end:
            found.append((start, end, category, data))
            last_end = end
    return found


def get_mask(
    category: str, data: str, journal: dict
) -> str:
    data = normalize(category, data)
    entries = journal.setdefault(category, {})
    if data not in entries:
        label = category.upper().replace(" ", "_")
        entries[data] = f"[{label}_{len(entries) + 1}]"
    return entries[data]


def anonymize(text: str, journal: dict) -> str:
    result = []
    pos = 0
    for start, end, category, data in find_data(text):
        result.append(text[pos:start])
        result.append(get_mask(category, data, journal))
        pos = end
    result.append(text[pos:])
    return "".join(result)


def load_journal() -> dict:
    try:
        return json.loads(read_file(JOURNAL_PATH))
    except FileError:
        return {}
    except json.JSONDecodeError:
        raise FileError(
            f"Журнал {JOURNAL_PATH} пошкоджено. Перевірте або видаліть його"
        )
