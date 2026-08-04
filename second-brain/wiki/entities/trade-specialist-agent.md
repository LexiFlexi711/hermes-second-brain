---
title: Trade Specialist Agent
type: entity
created: 2026-05-19
role: AI agent met focus op pullback-only crypto trading
---

# Trade Specialist Agent

## Rol
Senior pullback/bounce trade bot developer. Schrijft pullback-only scripts die stap-voor-stap leren winstgevend te worden.

## Entry Conditions (SHORT)
- 4H DOWN (lower highs/lower lows, bearish impulse, broken support)
- Bounce omhoog detecteren
- fib zone controleren
- 15M bearish bevestiging
- entry_lateness check

## Fib Zones
Zie [[pullback-trader-strategy]] voor fib zones tabel.

## Verboden
- "4H trend entry" als enige OPEN reden
- Fib <30% of >70%
- RR < 2.0
- noa_trader.py aanpassen
- Fees/slippage/extra indicatoren

## Bestand
`NOA-Reign/autonomous/agents/trade-specialist.md`

## Zie ook
- [[pullback-trader-strategy]]
- [[crypto-tradebot]]
