---
title: "Hermes Final Review Policy"
date: 2026-07-07
type: policy
source: HERMES AUDIT 03
status: active
---

# Hermes Final Review Policy

**Status:** actief
**Datum:** 2026-07-07
**Bron:** HERMES AUDIT 03 — Final review vóór repo-wijziging

## Besluit

Final-review discipline is goed genoeg, maar moet als vaste policy vastliggen.

Hermes doet recente repo-wijzigingen meestal correct:
- kleine gerichte commits
- git diff vóór commit
- backups vóór config/service wijzigingen
- geen commit/push zonder expliciet akkoord
- geen secrets of generated junk in recente commits
- Pro model blijft default voor reviewtaken

Belangrijk aandachtspunt: de reviewkwaliteit hangt nog deels af van Lexi's expliciete COMMITPROMPT. Daarom wordt deze policy vastgelegd als vaste werkregel.

## Harde regel

Hermes commit of pusht nooit zonder final review.

Final review betekent:
1. status tonen
2. diff tonen
3. tests/syntax waar mogelijk
4. secrets check
5. generated/junk check
6. risico's benoemen
7. rollbackpad tonen
8. expliciet akkoord vragen

## Vóór elke repo-wijziging

- Voer `git status` uit.
- Lees alleen relevante bestanden volgens de context-policy.
- Houd de wijziging minimaal.
- Geen brede refactor zonder expliciete scope.
- Geen generated/testdata/logs toevoegen tenzij expliciet gevraagd.

## Na wijziging, vóór commit

Verplicht tonen:
```bash
git status
git diff --stat
git diff
```

Waar mogelijk uitvoeren:
```bash
python -m compileall <relevante_paden>
pytest <relevante_tests>
bash -n <script.sh>
```

Afhankelijk van projecttype mag Hermes een passende syntax/test-check kiezen.

## Secrets check

Controleer diff/staged content op mogelijke secrets:
```bash
git diff --cached | grep -Ei "api_key|token|secret|password|authorization|bearer|private_key" || true
git diff | grep -Ei "api_key|token|secret|password|authorization|bearer|private_key" || true
```

Bij mogelijke secret: STOP, niets committen, Lexi waarschuwen, rollback of masking voorstellen.

## Generated/junk check

Voor commit controleren:
```bash
git diff --cached --name-only
git status --short
```

STOP bij staged of onverwachte bestanden zoals:
- `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- `*.pyc`, `*.log`, `*.sqlite`, `*.db`
- `logs/`, `l4_store/`
- grote gegenereerde output
- onbekende untracked bestanden

Tenzij Lexi expliciet zegt dat ze mee moeten.

## Vóór commit

Hermes toont:
- gewijzigde bestanden
- diffstat
- testresultaten
- secrets-check resultaat
- generated/junk-check resultaat
- risico's
- rollbackpad
- voorgestelde commit message

Hermes vraagt daarna expliciet akkoord. Geen akkoord = geen commit.

## Rollbackpad

Voor gewone codewijzigingen: `git checkout -- <bestand>`
Na commit: `git revert <commit>`
Voor config/service wijzigingen: eerst backup maken, backup-pad tonen, rollbackcommando tonen.

## Vóór push

Hermes toont verplicht:
```bash
git branch --show-current
git remote -v
git log --oneline -1
git status
```

En bevestigt: juiste branch? juiste remote? laatste commit klopt? tests groen? working tree clean? geen secrets? geen generated junk?

Daarna expliciet akkoord vragen. Geen akkoord = geen push.

## Stopregels

Hermes stopt onmiddellijk bij:
- onbekende untracked bestanden
- mogelijke secrets
- onverwachte brede diff
- meer dan 5 gewijzigde files zonder expliciete scope
- test failure
- syntax failure
- branch/remote onzekerheid
- generated files in staged changes
- `.sqlite`, `.db`, logs of stores in staged changes
- twijfel over opdracht/scope

## Acceptatietests

| Vraag | Verwacht gedrag |
|-------|----------------|
| "pas 1 script aan" | status → edit → diff → test → review → akkoord vragen vóór commit |
| "commit dit" | diff/test/secrets/branch tonen, daarna akkoord vragen |
| "push maar" | remote/branch/last commit/status tonen, daarna akkoord vragen |
| "fix config.yaml" | backup + diff + syntax waar mogelijk + rollbackpad |
| "grote refactor" | scope vragen of opdelen, niet blind uitvoeren |
| "generated files gewijzigd" | waarschuwing + stop tenzij expliciet gewenst |
| "tests falen" | geen commit/push |

## Do-not-change

Deze policy installeert niets en wijzigt niets aan:
- git hooks
- repo config
- model default
- MCP config
- runtime config
- bestaande code

## Regel voor toekomst

Een commit is pas klaar als Hermes kan uitleggen:
- wat veranderde
- waarom het veilig is
- hoe het getest is
- hoe het teruggedraaid wordt
