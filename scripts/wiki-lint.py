#!/usr/bin/env python3
"""
wiki-lint.py - Lint check for LLM Wiki markdown files.
Checks: missing frontmatter, broken wikilinks, orphan pages, stale inbox files.

Usage: python3 wiki-lint.py
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def extract_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        fm = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        return fm
    return None


def extract_wiki_links(content):
    cleaned = re.sub(r'\`\`\`.*?\`\`\`', '', content, flags=re.DOTALL)
    cleaned = re.sub(r'\`[^\`]+\`', '', cleaned)
    return set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', cleaned))


def get_all_doc_ids(wiki_path):
    ids = set()
    for md_file in wiki_path.rglob('*.md'):
        if md_file.name != 'index.md':
            ids.add(md_file.stem)
    return ids


def lint_wiki(base_path):
    wiki_path = base_path / 'wiki'
    inbox_path = base_path / 'raw' / 'inbox'
    issues = {'error': [], 'warning': [], 'info': []}

    all_ids = get_all_doc_ids(wiki_path)

    for md_file in wiki_path.rglob('*.md'):
        if md_file.name == 'index.md':
            continue

        content = md_file.read_text(encoding='utf-8')
        fm = extract_frontmatter(content)
        rel_path = str(md_file.relative_to(wiki_path))

        if fm is None:
            issues['error'].append(f"{rel_path}: missing frontmatter")
        else:
            if 'title' not in fm:
                issues['warning'].append(f"{rel_path}: missing title in frontmatter")
            if 'type' not in fm:
                issues['warning'].append(f"{rel_path}: missing type in frontmatter")
            elif fm['type'] not in ['concept', 'entity', 'source_summary', 'synthesis', 'log', 'index', 'project', 'fix', 'decision']:
                issues['warning'].append(f"{rel_path}: invalid type '{fm['type']}'")

        links = extract_wiki_links(content)
        broken = links - all_ids
        for link in broken:
            issues['warning'].append(f"{rel_path}: broken link [[{link}]]")

    # Orphan page detection: pages that exist but are linked by NO other page
    link_sources = defaultdict(set)  # target -> set of source files
    for md_file in wiki_path.rglob('*.md'):
        if md_file.name == 'index.md':
            continue
        content = md_file.read_text(encoding='utf-8')
        found_links = extract_wiki_links(content)
        for link in found_links:
            if link in all_ids:
                link_sources[link].add(md_file.stem)
    
    orphan_pages = []
    for page_id in sorted(all_ids):
        if page_id not in link_sources:
            # Find which file has this page_id
            for md_file in wiki_path.rglob('*.md'):
                if md_file.stem == page_id and md_file.name not in ('index.md', 'log.md'):
                    orphan_pages.append(md_file)
                    break
    
    for page in orphan_pages:
        rel_path = str(page.relative_to(wiki_path))
        issues['info'].append(f"{rel_path}: orphan page (nergens gelinkt)")

    if inbox_path.exists():
        threshold = datetime.now() - timedelta(days=7)
        for f in inbox_path.glob('*.md'):
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < threshold:
                issues['warning'].append(f"raw/inbox/{f.name}: stale (modified {mtime.strftime('%Y-%m-%d')})")

    return issues


def main():
    base_path = Path.home() / 'system' / 'second-brain'
    issues = lint_wiki(base_path)

    print(f"=== Wiki Lint Results ===")
    print(f"Errors: {len(issues['error'])}")
    print(f"Warnings: {len(issues['warning'])}")
    print(f"Info: {len(issues['info'])}")

    for level in ['error', 'warning', 'info']:
        for issue in issues[level]:
            print(f"  [{level.upper()}] {issue}")

    if issues['error']:
        exit(1)


if __name__ == '__main__':
    main()
