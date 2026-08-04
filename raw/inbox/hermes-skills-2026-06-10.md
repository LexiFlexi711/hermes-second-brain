---
title: Nieuwe Hermes skills (2026-06-10)
type: log
tags: [hermes, skills, update, dashboard, restart]
status: final
created: 2026-06-10
---

# Nieuwe Hermes skills

Op verzoek van Lexi twee skills aangemaakt:

## 1. hermes-self-update-check

`devops/hermes-self-update-check`

Checkt Hermes versie, changelog, update beschikbaarheid, en voert update veilig uit.

Huidige status: **Hermes Agent v0.16.0** (77 commits achter upstream).

## 2. hermes-dashboard-restart

`devops/hermes-dashboard-restart`

Vaste workflow voor kill → herstart → charts regenereren → verifiëren.

Geen `&` of `disown` — altijd `background=true`.
