#!/usr/bin/env python3
"""
wiki-index-gen.py — Genereert een voorstel of schrijft direct naar wiki/index.md
op basis van frontmatter in wiki/ subdirectories.

Usage: python3 ~/system/hermes-second-brain/scripts/wiki-index-gen.py          # voorstel naar stdout
       python3 ~/system/hermes-second-brain/scripts/wiki-index-gen.py --dry-run # enkel tellen
       python3 ~/system/hermes-second-brain/scripts/wiki-index-gen.py --write   # backup + overschrijf index.md
       python3 ~/system/hermes-second-brain/scripts/wiki-index-gen.py --write --dry-run  # backup zonder overschrijven
"""

import re
import sys
from pathlib import Path

WIKI_ROOT = Path.home() / "system" / "second-brain" / "wiki"
EXCLUDE_FILES = {"index.md", "log.md"}

def extract_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm

def slugify(path):
    """Convert path to wikilink format: lowercase, replace spaces/special chars."""
    name = path.stem
    # Keep alphanumeric and hyphens only
    name = re.sub(r'[^a-zA-Z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-').lower()
    return name

def scan_directory():
    sections = {}
    
    for subdir in sorted(WIKI_ROOT.iterdir()):
        if not subdir.is_dir():
            continue
        section_name = subdir.name.capitalize()
        entries = []
        
        for fpath in sorted(subdir.glob("*.md")):
            if fpath.name in EXCLUDE_FILES:
                continue
            
            content = fpath.read_text()
            fm = extract_frontmatter(content)
            title = fm.get("title", fpath.stem)
            link = slugify(fpath)
            
            # Try to get a short description from type or first line
            extra = ""
            fm_type = fm.get("type", "")
            if fm_type:
                extra = f" ({fm_type})"
            
            entries.append((link, title, extra))
        
        if entries:
            sections[section_name] = entries
    
    return sections

def generate_index(sections):
    lines = [
        "---",
        "title: Noa Second Brain Index (auto-gegenereerd voorstel)",
        "type: index",
        f"updated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "---",
        "",
        "# Noa Second Brain Index",
        "",
        "> ⚠️ Dit is een **automatisch voorstel**. Controleer of alle entries kloppen",
        "> voordat je de bestaande index.md vervangt.",
        "",
    ]
    
    for section_name in sorted(sections.keys()):
        lines.append(f"## {section_name}")
        lines.append("")
        for link, title, extra in sections[section_name]:
            lines.append(f"- [[{link}]] — {title}{extra}")
        lines.append("")
    
    return "\n".join(lines)

def main():
    dry_run = "--dry-run" in sys.argv
    do_write = "--write" in sys.argv
    
    print("=== wiki-index-gen.py ===", file=sys.stderr)
    print(f"Scannen: {WIKI_ROOT}", file=sys.stderr)
    
    sections = scan_directory()
    
    total = sum(len(e) for e in sections.values())
    for section, entries in sorted(sections.items()):
        print(f"  {section}: {len(entries)} entries", file=sys.stderr)
    print(f"  Totaal: {total} entries", file=sys.stderr)
    
    if do_write:
        index_path = WIKI_ROOT / "index.md"
        backup_path = WIKI_ROOT / "index.md.bak"
        
        # Backup
        if index_path.exists():
            import shutil
            shutil.copy2(str(index_path), str(backup_path))
            print(f"  Backup: {backup_path.name}", file=sys.stderr)
        
        if dry_run:
            print(f"  Modus: dry-run (zonder overschrijven)", file=sys.stderr)
        else:
            content = generate_index(sections)
            index_path.write_text(content)
            print(f"  Geschreven: {total} entries naar {index_path.name}", file=sys.stderr)
            print(f"  ✅ index.md bijgewerkt", file=sys.stderr)
    elif not dry_run:
        print(f"Modus: voorstel genereren (stdout)", file=sys.stderr)
        print(file=sys.stderr)
        print(generate_index(sections))

if __name__ == "__main__":
    main()