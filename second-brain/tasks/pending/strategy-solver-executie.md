# Taak: Bouw StrategySolver — Task 1 t/m 4

**Van:** Claude  
**Datum:** 2026-06-02  
**Prioriteit:** Hoog  
**Plan:** `/home/sjoe/.hermes/plans/2026-06-01_strategy-solver-plan.md`

---

## Context

Lexi keurt het StrategySolver plan goed. Je mag starten met executie.

Het plan bevat 6 taken. Bouw ze in volgorde, stap voor stap. Na elke taak: schrijf een tussenresultaat zodat ik kan reviewen voor je verdergaat.

Maar **begin met Task 1 t/m 4** — dat is de volledige werkende kern zonder LLM en zonder CLI. Die kunnen wachten.

---

## Twee spec-bugs in het plan — fix ze voor je begint

**Bug 1:** `SimulationResult` mist het veld `win_rate`. De `verify()` methode in Task 2 roept `result.win_rate` aan, maar de dataclass definieert alleen `winnaars` en `verliezers`. Voeg toe aan de dataclass:
```python
@property
def win_rate(self) -> float:
    return self.winnaars / self.aantal_trades if self.aantal_trades > 0 else 0.0
```
Of als plain field: `win_rate: float = 0.0` — zorg dat het correct berekend wordt in `forward_simulate`.

**Bug 2:** De test in Task 3 gebruikt `StrategyProposal(entry=100, sl=99, tp=102, ...)` maar de dataclass zegt `entry_price`. Gebruik `entry_price=100` in de test.

---

## Bestanden

**Target project:** `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/`

| Task | File aan te maken |
|------|------------------|
| Task 1 | `scripts/strategy_solver.py` |
| Task 2 | `scripts/strategy_solver.py` (uitbreiden) |
| Task 3 | `scripts/strategy_solver.py` (uitbreiden) |
| Task 4 | `scripts/backward_generator.py` + koppeling in `strategy_solver.py` |
| Tests  | `tests/unit/test_strategy_solver.py` |

---

## Wat te bouwen (Task 1 t/m 4)

### Task 1 — StrategySolver kernel
Bouw de dataclasses en de lege skeleton:
- `StrategyTarget`, `StrategyProposal`, `SimulationResult`, `VerificationFeedback`, `StrategySolution`
- Klasse `StrategySolver` met lege `backward_from_target`, `forward_simulate`, `verify`, `solve`
- Alle backward formules correct (zie plan)

### Task 2 — verify() implementeren
Implementeer de scoringslogica: 40% winst, 25% drawdown, 20% R:R, 15% win rate.
Adjustment hints in het Nederlands.
Convergentie: score >= (1 - convergence_threshold).

### Task 3 — forward_simulate() implementeren
Simuleer strategie op een lijst closes.
- Long only (voor nu — short komt later)
- Entry: zoek nearest index in closes
- SL / TP check per candle
- Drawdown bijhouden
- Forceer close op einde reeks
- Edge cases: lege closes → raise ValueError, SL >= TP → raise ValueError

### Task 4 — BackwardGenerator
Bouw `scripts/backward_generator.py`:
- Klasse `BackwardGenerator` met `generate(target, feedback=None)`
- Market regime aanpassing (range/trend/volatile)
- Feedback-gedreven aanpassing: als `adjustments` bevat "verbreed TP-target" → verhoog TP met 10%
- Koppel aan `StrategySolver.backward_from_target`

---

## Tests

Schrijf alle tests uit het plan in `tests/unit/test_strategy_solver.py`.
Voeg toe:
- `test_verify_win_rate_zero_trades` — aantal_trades=0 → geen crash
- `test_forward_simulate_empty_closes_raises`
- `test_forward_simulate_sl_equals_tp_raises`

Alle tests moeten slagen met `python -m pytest tests/unit/test_strategy_solver.py -v`.

---

## Constraints

- **Enkel stdlib** — geen pip install, geen numpy, geen pandas
- **Paper trading only** — geen exchange-calls, geen orders
- **Lexi beslist** — de solver adviseert, plaatst nooit automatisch
- Alle code in Nederlands gecommentarieerd (variabelnamen mogen Engels)
- Geen prints in de module zelf — alleen in de CLI (Task 6, later)
- Backward formules exact zoals in het plan — niet improviseren

---

## Bewijs dat je levert

1. `python -m pytest tests/unit/test_strategy_solver.py -v` — alle tests groen
2. Een kort demo-snippetje dat toont dat `solve()` werkt op een simpele reeks closes
3. Vermeld welke spec-bugs je gefixed hebt en hoe

---

## Mag niet

- Task 5 (LLM integratie) en Task 6 (CLI) nog niet bouwen
- Geen nieuwe dependencies installeren
- Niet raken aan de bestaande grid scripts of strategy code

