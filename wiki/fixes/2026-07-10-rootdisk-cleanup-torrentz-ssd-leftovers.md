# Fix: Rootdisk Cleanup — Torrentz SSD Leftovers

**Datum:** 2026-07-10
**Uitgevoerd door:** Noa (Hermes Agent) met Lexi's akkoord
**Status:** ✅ Afgerond

## Probleem

Rootdisk (`/dev/mapper/ubuntu--vg-ubuntu--lv`, 226G) steeg naar 75% (161G used, 56G vrij).

## Oorzaak

Oude handmatige/native Torrentz-downloads stonden op SSD in `/home/sjoe/dataLexi/Torrentz` (48G). Dit waren 10 film-items van juli 2025 — geen Docker qBittorrent downloads.

De Docker qBittorrent stond al correct geconfigureerd:
- `/mnt/otherdrive1/dataLexi/Torrentz/downloads` → `/downloads` (SATA)
- `/mnt/otherdrive1/qbittorrent/config` → `/config` (SATA)
- `DefaultSavePath=/downloads/`, `TempPath=/downloads/incomplete/`

## Acties

### 1. State-snapshot archive (557M)
- `/home/sjoe/.hermes/state-snapshots/` verplaatst naar `/mnt/otherdrive1/hermes-archive/state-snapshots/`
- `.env`, `auth.json`, `config.yaml` verwijderd uit archive (stonden 777 op fuseblk/NTFS met Samba-export)
- `state.db` backup blijft op SATA

### 2. Dubbele films (7 items, ~27G)
Verwijderd van SSD — stonden al op SATA in `/mnt/otherdrive1/dataLexi/Film/`:
- Superman 2025
- Nosferatu 2024
- John Wick Chapter 4
- Dief 1998
- Almost Cops 2025
- Unforgivable 2025
- Osiris 2025

### 3. Unieke films (3 items, ~20G)
Eerst via rsync naar SATA gekopieerd, geverifieerd (SHA256/dir compare), daarna SSD-bron verwijderd:
- Karate Kid Legends 2025 (19G)
- Captain Sabertooth (818M)
- Crimi Clowns Season 1 (814M)

## Resultaat

| Moment | Used | Vrij | % |
|--------|------|------|---|
| Voor cleanup | 161G | 56G | 75% |
| Na cleanup | 113G | 103G | 53% |

**Totaal vrijgekomen: ~48G**

## Huidige staat

- `/home/sjoe/dataLexi/Torrentz/` — leeg (4.0K)
- qBittorrent Docker: alle paths → SATA via `/downloads/`
- Films op SATA: `/mnt/otherdrive1/dataLexi/Film/`
- State.db: NIET aangeraakt, live op SSD

## Waarschuwingen

- Geen delete op `/mnt/otherdrive1` uitgevoerd
- `/home/sjoe/dataLexi/Torrentz/` niet meer gebruiken voor handmatige downloads
- qBittorrent paths blijven op SATA — niet wijzigen zonder deze note te updaten

## Volgende checks

- [x] qBit paths geverifieerd op SATA
- [x] `/home/sjoe/dataLexi/Torrentz` leeg
- [ ] NeuroAPI MCP tools auditen
- [ ] Self-improvement review audit
- [ ] Filesystem MCP hardening controleren
