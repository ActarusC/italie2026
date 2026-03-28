#!/usr/bin/env python3
"""
Génère une version portable du site (un seul fichier HTML).

Les notes markdown sont inlinées dans le JavaScript, ce qui
élimine les appels fetch() et permet d'ouvrir le fichier
directement dans un navigateur mobile sans serveur local.

Usage:
    python3 build-portable.py
    # → produit italie2026-portable.html
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "index.html"
OUT = ROOT / "italie2026-portable.html"


def main():
    html = SRC.read_text(encoding="utf-8")

    # Extraire tous les noteFile référencés dans le JS
    note_files = re.findall(r'noteFile:\s*"([^"]+)"', html)

    # Lire chaque fichier markdown
    cache_entries = []
    for nf in note_files:
        path = ROOT / nf
        if path.exists():
            md = path.read_text(encoding="utf-8")
            cache_entries.append(f"  {json.dumps(nf)}: {json.dumps(md)}")
        else:
            print(f"  ⚠ fichier introuvable: {nf}", file=sys.stderr)

    # Construire le notesCache pré-rempli
    cache_js = "const notesCache = {\n" + ",\n".join(cache_entries) + "\n};"

    # Remplacer la ligne vide du cache
    html = html.replace("const notesCache = {};", cache_js)

    OUT.write_text(html, encoding="utf-8")

    n = len(cache_entries)
    size_kb = OUT.stat().st_size / 1024
    print(f"✓ {OUT.name} généré ({n} notes inlinées, {size_kb:.0f} Ko)")


if __name__ == "__main__":
    main()
