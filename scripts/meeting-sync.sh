#!/usr/bin/env bash
# meeting-sync.sh — Synchroniseer nieuwe meetings naar 2nd brain
# Gebruik: bash ~/system/hermes-second-brain/scripts/meeting-sync.sh
#
# Wat: Kopieert nieuwe meeting .md en .json bestanden van
#       ~/Noa-Hermes/autonomous/meetings/ naar
#       ~/system/second-brain/wiki/synthesis/
#       en updatet index.md + log.md.
#
# Manueel gebruik: na elke meeting even draaien.
# Geen cron — jij beslist wanneer.

set -euo pipefail

# --- Config ---
MEETINGS_DIR="$HOME/Noa-Hermes/autonomous/meetings"
SYNTHESIS_DIR="$HOME/system/second-brain/wiki/synthesis"
INDEX_FILE="$HOME/system/second-brain/wiki/index.md"
LOG_FILE="$HOME/system/second-brain/wiki/log.md"
LINT_SCRIPT="$HOME/system/hermes-second-brain/scripts/wiki-lint.py"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Meeting Sync ==="
echo "Bron:      $MEETINGS_DIR"
echo "Doel:      $SYNTHESIS_DIR"
echo ""

# --- Stap 1: Vind nieuwe meetings ---
synced=0
skipped=0

for meeting_file in "$MEETINGS_DIR"/*.md; do
    [ -f "$meeting_file" ] || continue
    
    basename_file=$(basename "$meeting_file")
    target_file="$SYNTHESIS_DIR/$basename_file"
    json_file="${meeting_file%.md}.json"
    target_json="$SYNTHESIS_DIR/${basename_file%.md}.json"
    
    if [ -f "$target_file" ]; then
        # Check of het bestand in synthesis ouder is dan in meetings
        if [ "$meeting_file" -nt "$target_file" ]; then
            # Kopieer en overschrijf
            cp "$meeting_file" "$target_file"
            echo -e "  ${YELLOW}🔄 ${basename_file} (bijgewerkt)${NC}"
        else
            echo -e "  ${GREEN}✅ ${basename_file} (al gesynced)${NC}"
            skipped=$((skipped + 1))
            continue
        fi
    else
        cp "$meeting_file" "$target_file"
        echo -e "  ${GREEN}✅ ${basename_file} (nieuw)${NC}"
    fi
    
    # Kopieer JSON als die bestaat
    if [ -f "$json_file" ]; then
        target_json_name="${basename_file%.md}.json"
        target_json_path="$SYNTHESIS_DIR/$target_json_name"
        if [ ! -f "$target_json_path" ] || [ "$json_file" -nt "$target_json_path" ]; then
            cp "$json_file" "$target_json_path"
            echo -e "  ${GREEN}✅ ${target_json_name}${NC}"
        fi
    fi
    
    synced=$((synced + 1))
    
    # --- Stap 2: Haal titel uit frontmatter ---
    title=$(awk '/^---$/{flag=1; next} /^---$/{flag=0} flag && /^title:/{print substr($0, index($0,$2))}' "$target_file" | head -1 | sed 's/^"//;s/"$//')
    if [ -z "$title" ]; then
        title="${basename_file%.md}"
    fi
    
    # --- Stap 3: Update index.md (Synthesis sectie) ---
    link_name="${basename_file%.md}"
    # lowercase voor wikilink
    link_lower=$(echo "$link_name" | tr '[:upper:]' '[:lower:]')
    
    if ! grep -q "\[\[$link_lower\]\]" "$INDEX_FILE" 2>/dev/null; then
        # Voeg toe aan Synthesis sectie (voor de laatste entry)
        sed -i "/^## Synthesis$/,/^## /{ /^## Source/!{ /^## /!s/^## Source.*$/## Source\n- [[$link_lower]] — $title\n&/ } }" "$INDEX_FILE" 2>/dev/null || true
        # Eenvoudigere aanpak: voeg na de laatste synthesis entry toe
        sed -i "0,/^- \[\[team-meeting-009-pullback-audit\]\]/s//- [[$link_lower]] — $title\n- [[team-meeting-009-pullback-audit]]/" "$INDEX_FILE" 2>/dev/null || true
        echo -e "  ${GREEN}📝 index.md: toegevoegd [[$link_lower]]${NC}"
    fi
    
    # --- Stap 4: Update log.md ---
    today=$(date +%Y-%m-%d)
    log_entry="- Aangemaakt/gesynced: \`wiki/synthesis/$basename_file\` — $title"
    
    if grep -q "^## $today" "$LOG_FILE" 2>/dev/null; then
        # Vandaag bestaat al in log — voeg entry toe na de datumregel
        sed -i "/^## $today/a\\\n$log_entry" "$LOG_FILE" 2>/dev/null || true
    else
        # Nieuwe datum entry
        echo -e "\n## $today\n\n$log_entry" >> "$LOG_FILE"
    fi
    echo -e "  ${GREEN}📝 log.md: entry toegevoegd${NC}"
done

# --- Stap 5: Rapport ---
echo ""
echo "=== Resultaat ==="
echo -e "  ${GREEN}Gesynced: $synced${NC}"
echo -e "  ${GREEN}Al bekend: $skipped${NC}"

# --- Stap 6: Lint ---
echo ""
echo "=== Lint Check ==="
if [ -f "$LINT_SCRIPT" ]; then
    python3 "$LINT_SCRIPT" || true
else
    echo -e "  ${YELLOW}⚠️ Lint script niet gevonden op $LINT_SCRIPT${NC}"
fi

echo ""
echo "✅ Meeting sync voltooid."