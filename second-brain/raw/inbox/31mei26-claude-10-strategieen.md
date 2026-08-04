---
title: "10 beste crypto-bot strategieën — feedback & onderzoek"
type: source_summary
created: 2026-05-31
source: Claude Code (Lexi's prompt "gaat dit eesn bekjken op het net")
status: inbox
---

# 10 Beste Crypto-Bot Strategieën — Onderzoek & Feedback

> Bewaard op vraag van Lexi: 31mei26claudelezen
> Bron: Hermes (Noa) research + Claude Code voorstel

## Overzichtstabel

| # | Strategie | Vonnis | Timing |
|---|-----------|--------|--------|
| 1 | Adaptive trend-following / momentum | ✅ NU: Hoofdstrategie | Deze week |
| 2 | Relative strength / coin rotation | ✅ NU: Filter vóór entry | Deze week |
| 3 | Breakout + volatility/volume confirmatie | ⚠️ Nuanceren: sub-entry binnen trend | Fase 3 |
| 4 | Dynamic grid trading | ✅ Na regime detector | Fase 4 |
| 5 | Range mean reversion | ⚠️ Alleen met streng range filter | Fase 4 |
| 6 | Failed breakout / liquidity trap | 🏆 QUICK WIN: exit layer | DEZE WEEK |
| 7 | Market making / spread capture | ❌ KILLEN | Nooit voor deze bot |
| 8 | Funding-rate / spot-perp arbitrage | ⏳ Later: na data pipeline upgrade | Ver later |
| 9 | Pairs/statistical arbitrage | ❌ KILLEN | Nooit voor deze bot |
| 10 | ML/regime-classifier + meta-selector | ⏳ Later: eerst rule-based | Fase 5 |

## 🔬 Bronnen per strategie

### 1. Momentum / trend-following
- **arXiv 2602.11708** (Feb 2026): "Systematic Trend-Following with Adaptive Portfolio Construction" — AdaptiveTrend framework, 150+ crypto pairs, 36 maanden OOS (2022-2024). Sharpe 2.41, max DD -12.7%. H6 momentum + ATR trailing stop + 70/30 long/short.
- **QuantifiedStrategies** (Bitcoin 2015-2021): 20-day EMA trend = 126% CAGR, PF 2.69, WR 33%. Momentum 25-day = PF 3.84.
- **Conclusie:** Momentum outperforms pullback consistent. Jouw V3A: 29% WR, negatieve P&L. Momentum: 52% WR, +123% P&L.

### 2. Relative strength / coin rotation
- **StockCharts**: RRG werkt op crypto (coherente asset groep)
- **Weiss Ratings**: documenteert BTC → ETH → altcoin rotatie
- **Conclusie:** Beste filter. Geen relative strength edge = geen trade.

### 3. Breakout + volume confirmatie
- **Reddit r/algotrading**: Bitcoin breakout 65.92% CAGR sinds 2014
- **PyQuantLab**: volatility breakout met volume confirmatie
- **Risico:** 60% van breakouts zijn fakeouts (3-day confirmation filtert 60% valse signalen)

### 4. Dynamic grid trading
- **arXiv 2506.11921** (Jun 2025): "Dynamic Grid Trading Strategy" — traditionele grid = zero expected return. DGT: IRR 78%, Sharpe 1.4, max DD 18% op BTC/ETH minuutdata 2021-2024. Open source.
- **Conclusie:** Alleen dynamisch. Statisch is dom.

### 5. Range mean reversion
- **QuantifiedStrategies**: Bitcoin mean reversion outperformt momentum in low volume regimes
- **Hurst exponent BTC (2021-2024)**: 0.52 (mild trending, geen sterke reversion)
- **Changelly**: 0.4% moves verdwijnen na fees + spread + slippage
- **Conclusie:** Werkt alleen met streng range filter. Niet voor fase 1.

### 6. Failed breakout / liquidity trap
- **Fortraders**: "False Breakouts — Why They Happen and How to Trade Them"
- **ChartScout**: 3-step guide voor fakeouts in crypto
- **Binance**: "Fake Breakouts: The #1 Trap That Wrecks Traders"
- **Conclusie:** GROOTSTE QUICK WIN. Geen nieuwe data nodig. Exit layer.

### 7. Market making / spread capture
- **Hummingbot**: open-source framework (bestaat al)
- **DWF Labs**: 4 core market making strategieën
- **arXiv 2504.16542**: stochastic optimization voor liquidity provision
- **Conclusie:** KILL. Niet voor directional bot. Hummingbot bestaat al.

### 8. Funding rate / spot-perp arbitrage
- **ScienceDirect** (Aug 2025): "Risk and Return Profiles of Funding Rate Arbitrage" — 60 scenarios, returns tot 115.9%/6mnd, max loss 1.92%. Geen correlatie met HODL.
- **ChainStack docs**: implementatie guide
- **Conclusie:** Zakelijk sterk, maar complex. Vereist perp data + funding feeds.

### 9. Pairs trading / statistical arbitrage
- **EUR Thesis**: positieve excess returns, maar onder aandelen-literatuur
- **Amberdata**: cointegration beats correlation
- **Conclusie:** KILL. Crypto-relaties breken te vaak.

### 10. ML/regime-classifier
- **GitHub akash-kumar5**: HMM + LSTM voor regime detectie
- **Springer** (2025): ML ensemble modellen voor crypto
- **Reddit r/algotrading**: "ML voor regime detectie werkt beter dan directe predictie"
- **Conclusie:** Eerst rule-based regime detectie, dan pas ML. Fase 5.

## 🏆 Aanbevolen roadmap

1. **DEZE WEEK:** Failed breakout exit engine (geen nieuwe data nodig)
2. **DEZE WEEK:** Relative strength filter (pre-entry)
3. **VOLGENDE WEEK:** Momentum als hoofdstrategie
4. **FASE 3:** Breakout als sub-entry binnen trend
5. **FASE 4:** Range engine + dynamic grid
6. **FASE 5:** ML regime classifier
