# Layer 8 — Market Context Baseline

**Datum:** 2026-06-16
**Status:** L8A code-baseline frozen
**Auteur:** Noa (Hermes Agent)
**Akkoord:** Lexi

---

## Commitlijst

| Commit | Hash | Beschrijving |
|--------|------|-------------|
| L8A MVP | `f459df6b` | `feat(layer8): add market context MVP` |
| L8A.1 hardening | `b3c495bd` | `refactor(layer8): neutralize market context enums` |
| L8A.3 final | `80ee900f` | `refactor(layer8): split benchmark behavior and audit window` |

Tussenliggende L8A.2 is samen met L8A.3 gecommit.

---

## Doel van Layer 8

Layer 8 vergelijkt een coin met BTC en ETH over hetzelfde gesloten candlevenster.

L8 is een **benchmark-thermometer**. Hij vertelt of een coin met BTC/ETH meebeweegt, tegen BTC/ETH ingaat, of relatief sterker/zwakker beweegt. Hij beslist niets.

---

## Wat L8 wel zegt

1. Wat BTC en ETH doen (richting + return percentage)
2. Of de coin dezelfde richting beweegt als BTC/ETH (`direction_alignment`)
3. Of de coin sterker, zwakker, gemengd of ongeveer gelijk beweegt tegenover BTC/ETH (`relative_behavior`)
4. Of BTC en ETH in lijn of tegengesteld bewegen (`market_wind`)
5. Hoeveel candles effectief gebruikt zijn (`audit_window.candles_used`)
6. Hoeveel candles er beschikbaar waren (`audit_window.available_candles`)
7. Welke benchmarkdata beschikbaar was (`benchmark_availability`, `benchmark_mode`)
8. Of de pair zichzelf als benchmark gebruikt (`self_benchmark`)

---

## Wat L8 niet zegt

- kopen
- verkopen
- long
- short
- entry
- exit
- setup
- signaal
- timing
- voorspelling
- of iets een goede trade is
- correlation
- beta
- nieuws/catalysts
- trade-edge

---

## Outputvelden en hun betekenis

| Veld | Type | Betekenis |
|------|------|-----------|
| `pair` | string | Bijv. SOLEUR |
| `timeframe` | int | Minuten (5, 15, 60, 240, 1440) |
| `enabled` | bool | False bij fout |
| `quality` | string | `clean` / `warning` / `error` |
| `reasons` | list[str] | Fout- of waarschuwingsredenen |
| `self_benchmark` | `"btc"|"eth"|"none"` | BTCEUR→btc, ETHEUR→eth |
| `benchmark_availability` | `{btc, eth: bool}` | Welke benchmarks data hebben |
| `benchmark_mode` | `"both"|"btc_only"|"eth_only"|"none"` | Operationele modus |
| `lookback_candles` | int | 100 (MVP-config) |
| `relative_threshold_pct` | float | 0.5 (MVP-config) |
| `pair_return_pct` | float\|None | Return over gesloten venster |
| `btc_return_pct` | float\|None | Return over gesloten venster |
| `eth_return_pct` | float\|None | Return over gesloten venster |
| `pair_direction` | `up|down|sideways|unknown` | Richting van de coin |
| `btc_direction` | `up|down|sideways|unknown` | Richting van BTC |
| `eth_direction` | `up|down|sideways|unknown` | Richting van ETH |
| `relative_strength_vs_btc` | `outperforming|underperforming|in_line|unknown` | Pair vs BTC |
| `relative_strength_vs_eth` | `outperforming|underperforming|in_line|unknown` | Pair vs ETH |
| `direction_alignment` | `aligned_with_benchmark|diverging_from_benchmark|mixed_alignment|unknown` | Richting vs benchmarks |
| `relative_behavior` | `stronger_than_benchmarks|weaker_than_benchmarks|mixed_vs_benchmarks|in_line_with_benchmarks|unknown` | Magnitude vs benchmarks |
| `market_wind` | `benchmark_up|benchmark_down|benchmark_flat|benchmark_mixed|unknown` | BTC/ETH onderling |
| `audit_window.requested_lookback_candles` | int | 100 |
| `audit_window.lookback_span_minutes` | int | 100 × timeframe |
| `audit_window.candles_used` | `{pair, btc, eth: int}` | Effectief gebruikt (getrimd tot LOOKBACK) |
| `audit_window.available_candles` | `{pair, btc, eth: int}` | Beschikbaar voor trim |
| `audit_window.window_start` | `{pair, btc, eth: timestamp}` | Eerste candle van getrimd venster |
| `audit_window.window_end` | `{pair, btc, eth: timestamp}` | Laatste gesloten candle |
| `audit_window.last_closed_timestamp` | `{pair, btc, eth: timestamp}` | = window_end |
| `closed_candle_policy` | string | `"excludes candles[-1]"` |

---

## Live voorbeelden (2026-06-16)

### SOLEUR 60m — aligned + stronger

```
pair_return_pct: +10.6118
btc_return_pct:   +4.5427
eth_return_pct:   +5.8203

direction_alignment: aligned_with_benchmark
relative_behavior:   stronger_than_benchmarks
```

**Betekenis:** SOL bewoog dezelfde richting uit als BTC/ETH, maar sterker dan beide benchmarks.

### ADAEUR 60m — aligned + weaker

```
pair_return_pct: +3.7866
btc_return_pct:   +4.5427
eth_return_pct:   +5.8203

relative_behavior: weaker_than_benchmarks
```

**Betekenis:** ADA steeg mee met de markt, maar bleef achter op BTC en ETH.

### PEPEEUR 60m — aligned + mixed

```
pair_return_pct: +5.2371
btc_return_pct:   +4.5427
eth_return_pct:   +5.8203

relative_behavior: mixed_vs_benchmarks
```

**Betekenis:** PEPE was sterker dan BTC, maar zwakker dan ETH.

### DOGEEUR 60m — aligned + weaker

```
pair_return_pct: +1.3116
btc_return_pct:   +4.5427
eth_return_pct:   +5.8203

relative_behavior: weaker_than_benchmarks
```

**Betekenis:** DOGE steeg mee, maar duidelijk zwakker dan BTC/ETH.

### SOLEUR 240m — aligned + mixed

```
pair_return_pct: -10.1949
btc_return_pct:   -9.8374
eth_return_pct:  -11.5654

market_wind:           benchmark_down
direction_alignment:   aligned_with_benchmark
relative_behavior:     mixed_vs_benchmarks
```

**Betekenis:** SOL, BTC en ETH daalden allemaal. SOL bewoog ongeveer mee met BTC, maar daalde minder hard dan ETH. Daarom gemengd.

---

## Bekende grenzen

- **LOOKBACK=100** is MVP-config, niet per timeframe geoptimaliseerd
- **THRESHOLD_PCT=0.5** is MVP-config, schaalt niet met volatiliteit
- **Geen correlation of beta** — L8 vergelijkt enkel richting en return
- **Geen nieuws of catalysts** — L8 is candle-only
- **Geen L9-validatie** — L9 mag pas starten nadat L8 bewezen is
- **Geen tradebeslissing** — L8 is thermometer, geen dokter
- **Geen voorspelling** — L8 kijkt alleen naar gesloten candles

---

## Freeze-regel

L8 wordt **niet verder uitgebreid** zonder:

1. een concrete fout in live output, **of**
2. expliciet akkoord van Lexi.

Nieuwe ideeën zoals correlation, beta, nieuws, dashboard of Layer 9 horen **niet meer in L8A**. Als die ooit komen, worden het aparte lagen.

L8A is klaar, gebouwd, getest (48/48 + 261/261), live gesmoked, en gebaselined.

---

## Bestanden

```
projects/hermes-v01/director/hermes_director.py        — read_layer8()
projects/hermes-v01/layer8_market_context/__init__.py  — package marker
projects/hermes-v01/layer8_market_context/market_context.py — pure + wrapper
projects/hermes-v01/tests/test_layer8_market_context.py — 48 tests
```
