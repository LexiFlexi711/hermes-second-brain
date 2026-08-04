---
type: fix
title: status_overview.py — RAM-column fix
date: 2026-05-25
tags: [status, monitoring, ram, fix]
---

# status_overview.py — RAM-column fix

## Wat was er fout
`check_server()` in `/home/sjoe/scripts/status_overview.py` gebruikte `$5` uit `free -h` als "vrij geheugen". Kolom `$5` is **shared** memory, niet available.

## Wat is er aangepast
- **Bestand:** `/home/sjoe/scripts/status_overview.py` (lijn 90)
- **Oud:** `free -h | awk '/^Mem:/ {print $3, $5, $2}'`
- **Nieuw:** `free -h | awk '/^Mem:/ {print $3, $7, $2}'`
- `$3` = used, `$7` = available, `$2` = total

## Waarom
Linux `free -h` layout:
```
              total  used  free  shared  buff/cache  available
$1="Mem:"     $2     $3    $4    $5      $6          $7
```
`$7` (available) is de juiste kolom — da's wat écht vrij is inclusief reclaimable cache. `$5` (shared) was misleidend laag.

## Backup
`/home/sjoe/scripts/status_overview.py.bak.2026-05-25-1458`

## Testresultaat
Na fix: `ram: 6.2Gi/15Gi (vrij: 9.3Gi)` — correct.
Voorheen toonde het `(vrij: 27Mi)` — da's shared memory, niet wat vrij is.
