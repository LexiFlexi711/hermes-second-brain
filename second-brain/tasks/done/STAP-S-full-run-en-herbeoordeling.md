---
type: task
created: 2026-05-30
assignee: Hermes
priority: high
status: pending
depends_on: STAP-R
---

# STAP S — Volledige 7-pair run + herbeoordeling V3A

## Context

STAP-R heeft `v3a_multi_pair.py` herschreven met BacktestReader (historische CSV + archive).
ETHEUR test toont nu 89 trades (was 8) — WR 28%, PnL -44%, spread 19.6% (instabiel).

Nu alle 7 pairs draaien en STAP-Q herbeoordeling updaten met echte data.

## Deel 1 — Volledige multi-pair run

Draai het script voor alle 7 pairs:

```bash
cd /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3
python -m crypto_test_bot_v3.research.compare.v3a_multi_pair --verbose
```

Dit duurt lang (7 pairs × 3 varianten × 3 jaar data). Laat draaien.

Sla de output op als:
`tasks/done/STAP-S-multi-pair-output.txt` (kopieer de terminaloutput)

## Deel 2 — Kandidaatbeoordeling updaten

Bestand: `src/crypto_test_bot_v3/research/v3a_kandidaat_rapport.py`

Dit bestand bestaat al maar is gebaseerd op de oude data.
Update het zodat het de nieuwe JSON leest:
`logs/research/v3a_multi_pair_2026-05-30.json`

De nieuwe JSON heeft een ander formaat — Runner output ipv backtest_pair output.
Relevante keys per pair/variant:
- `results[pair][variant]["total_trades"]`
- `results[pair][variant]["winrate_pct"]`
- `results[pair][variant]["total_pnl_pct"]`
- `results[pair][variant]["max_loss_streak"]`

Criteria (zelfde als STAP-Q):
1. Consistentie: WR ≥ 40% op ≥ 4 van de 7 pairs (baseline)
2. Stabiliteit: gem. WR spread ≤ 15% over varianten
3. Paper/backtest: STAP-P was niet beoordeelbaar — markeer als "niet beschikbaar"
4. Exit potentieel: MFE/MAE data uit STAP-L/M (ongewijzigd)

## Verificatie

```bash
python -m pytest tests/ -q   # 60+ tests groen
python -m crypto_test_bot_v3.research.v3a_kandidaat_rapport
```

## Resultaat wegschrijven

`tasks/done/STAP-S-result.md`

Vermeld:
- Trade counts per pair
- WR% per pair baseline
- Eindoordeel: KANDIDAAT / NIET KLAAR / CONDITIONEEL
- Wat er specifiek aangepakt moet worden als niet klaar

## Niet doen

- Geen aanpassingen aan strategy-logica
- Geen nieuwe parameters
- Geen nieuwe backtest-engine
