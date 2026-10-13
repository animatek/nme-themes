#!/usr/bin/env python3
"""Checks every theme in themes/ and writes index.json, the list Animatek NME reads.

    python3 tools/build_index.py           # check, then write index.json
    python3 tools/build_index.py --check   # check only (pull requests)

Files starting with "_" (the template) are skipped. Standard library only.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
INDEX = ROOT / "index.json"

FORMAT = 1
MAX_BYTES = 256 * 1024          # NME refuses bigger files
FILE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.json$")
COLOUR = re.compile(r"^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
# NME's own themes: a community theme with one of these names would be renamed on install.
BUILTIN = {"nomad", "dark", "deep dark", "tokyo night", "gruvbox dark", "dracula", "nord",
           "ghosty", "magnetic revival", "mothwig", "macchiato", "cubitwig", "nord classic",
           "animatek rack"}


def check_colours(section, where, errors):
    if section is None:
        return
    if not isinstance(section, dict):
        errors.append(f"{where} is not an object")
        return
    for key, value in section.items():
        if key == "morphColor":
            if not isinstance(value, list) or not all(isinstance(v, str) and COLOUR.match(v) for v in value):
                errors.append(f"{where}.morphColor must be a list of colours")
        elif key == "canvasTexture":
            if not isinstance(value, bool):
                errors.append(f"{where}.canvasTexture must be true or false")
        elif not (isinstance(value, str) and COLOUR.match(value)):
            errors.append(f"{where}.{key} is not a colour: {value!r}")


def check_render(render, errors):
    if render is None:
        return
    if not isinstance(render, dict):
        errors.append("render is not an object")
        return
    for key, value in render.items():
        if key in ("wireframe", "hardwareLook", "flatKnobs"):
            if not isinstance(value, bool):
                errors.append(f"render.{key} must be true or false")
        elif key == "knobStyle":
            if not (isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 2):
                errors.append("render.knobStyle must be 0, 1 or 2")
        else:
            errors.append(f"render.{key} is not a render option")


def read_theme(path, errors):
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        errors.append(f"bigger than {MAX_BYTES // 1024} KB")
        return None, data
    if not FILE_NAME.match(path.name):
        errors.append("file name must be lowercase words joined by dashes, ending in .json")
    try:
        theme = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        errors.append(f"not valid JSON: {e}")
        return None, data
    if not isinstance(theme, dict):
        errors.append("not a JSON object")
        return None, data
    if theme.get("format") != FORMAT:
        errors.append(f'"format" must be {FORMAT}')
    name = theme.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append('"name" is missing')
    elif name.strip().lower() in BUILTIN:
        errors.append(f'"{name}" is the name of a theme NME already has')
    for key in ("author", "description", "base"):
        if key in theme and not isinstance(theme[key], str):
            errors.append(f'"{key}" must be text')
    check_colours(theme.get("app"), "app", errors)
    check_colours(theme.get("canvas"), "canvas", errors)
    check_render(theme.get("render"), errors)
    return theme, data


def main():
    check_only = "--check" in sys.argv[1:]
    entries, failed, seen = [], False, {}
    for path in sorted(THEMES.glob("*.json")):
        if path.name.startswith("_"):
            continue
        errors = []
        theme, data = read_theme(path, errors)
        if theme is not None and isinstance(theme.get("name"), str):
            key = theme["name"].strip().lower()
            if key in seen:
                errors.append(f'"{theme["name"]}" is also the name in {seen[key]}')
            seen.setdefault(key, path.name)
        if errors:
            failed = True
            for e in errors:
                print(f"themes/{path.name}: {e}")
            continue
        entry = {"name": theme["name"].strip(), "file": path.name}
        for key in ("author", "description"):
            if theme.get(key, "").strip():
                entry[key] = theme[key].strip()
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        entry["size"] = len(data)
        entries.append(entry)

    if failed:
        sys.exit(1)
    entries.sort(key=lambda e: e["name"].lower())
    print(f"{len(entries)} theme(s) OK")
    if check_only:
        return
    text = json.dumps({"format": FORMAT, "themes": entries}, indent=2, ensure_ascii=False) + "\n"
    if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != text:
        INDEX.write_text(text, encoding="utf-8")
        print("index.json written")


if __name__ == "__main__":
    main()
