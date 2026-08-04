---
type: task
created: 2026-05-31
assignee: Hermes
priority: normal
status: pending
---

# STAP V — Implementeer dezelfde 10 superpower skills voor Hermes

## Context

Claude heeft 10 nieuwe skills gekregen gebaseerd op de 10 superpower skills voor winstgevend algo-trading.
Hermes moet dezelfde skills krijgen zodat ze ze ook kan uitvoeren wanneer Lexi dat vraagt.

## De 10 skills (al aangemaakt door Claude in project)

De SKILL.md bestanden staan in:
```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/.claude/skills/
  crypto-backtest-auditor/SKILL.md     (superpower 1)
  crypto-regime-detector/SKILL.md      (superpower 2)
  crypto-structure-reader/SKILL.md     (superpower 3)
  crypto-risk-manager/SKILL.md         (superpower 4)
  crypto-stats-validator/SKILL.md      (superpower 5)
  crypto-cost-analyzer/SKILL.md        (superpower 6)
  crypto-testbot-health/SKILL.md       (superpower 7)
  crypto-journal-visual/SKILL.md       (superpower 8)
  crypto-strategy-monitor/SKILL.md     (superpower 9)
  crypto-strategy-researcher/SKILL.md  (superpower 10)
```

## Taak: kopieer de skills naar Hermes' skill-directory

Hermes moet deze skills kunnen uitvoeren. Kopieer de SKILL.md bestanden naar:
```
/home/sjoe/system/hermes-second-brain/second-brain/skills/
```

Maak per skill een submap aan, bv:
```
skills/crypto-backtest-auditor/SKILL.md
skills/crypto-regime-detector/SKILL.md
... etc
```

## Aanpassing per skill

Pas in elke SKILL.md het volgende aan voor Hermes' context:
- Vervang verwijzingen naar "Claude" door "Hermes" waar van toepassing
- Voeg toe aan elke skill: **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**
- Bewaar de paden en regels exact zoals ze zijn

## Verificatie

```bash
ls /home/sjoe/system/hermes-second-brain/second-brain/skills/
# moet 10 submappen tonen
```

## Resultaat wegschrijven

`tasks/done/STAP-V-result.md`

Vermeld: welke skills aangemaakt, welke aanpassingen gemaakt.
