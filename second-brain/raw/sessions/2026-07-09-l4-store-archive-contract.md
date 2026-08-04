# L4 STORE ARCHIVE CONTRACT v2 — 3 MONTHS UNZIPPED + WAL + QUERY GAP + CADENCE

**Datum:** 2026-07-09
**Status:** Contract v2, nog niet uitgevoerd

## 1. Beslissing

De L4 store bewaart altijd de laatste 3 kalendermaanden ongecomprimeerd.

Alles ouder dan die rolling 3-month window mag worden gecomprimeerd naar:
`<YYYY-MM>.sqlite.gz`

Geen dedup-wijziging. Geen raw_hash-wijziging. Geen DB-schema-wijziging.

## 2. Definitie rolling window

De actieve maand wordt altijd ongecomprimeerd gehouden.

Huidige maand 2026-07 — ongecomprimeerd:
- 2026-07.sqlite
- 2026-06.sqlite
- 2026-05.sqlite

Archiveren: 2026-04.sqlite en ouder.

Bij volgende maand 2026-08 — ongecomprimeerd:
- 2026-08.sqlite
- 2026-07.sqlite
- 2026-06.sqlite

Archiveren: 2026-05.sqlite en ouder.

## 3. Waarom

- Dedup/raw_hash aanpassen is een architectuurbeslissing
- Data is correct, 0% dedup door volatile source velden in raw_json
- Storagegroei is beheersbaar: 26 pairs × 3 maanden ≈ 58.5 GB raw
- Gzip archivering is veiliger dan nu het hash-contract wijzigen

## 4. Storage projectie 3 maanden unzipped

### 4.1 Raw (ongearchiveerd)

| Pairs | GB/maand | 3 maanden |
|------:|---------:|----------:|
| 2 | 1.5 GB | 4.5 GB |
| 4 | 3 GB | 9 GB |
| 10 | 7.5 GB | 22.5 GB |
| 26 | 19.5 GB | 58.5 GB |

### 4.2 Gemeten compressie

Gemeten op echte productie-DB (2026-07 ETHEUR):
- 31.5 MB SQLite
- 4.5 MB gzip
- compressieratio: ~7.0x

| Raw | Gzip bij 7.0x |
|---------:|--------------:|
| 4.5 GB | ±0.64 GB |
| 9 GB | ±1.29 GB |
| 22.5 GB | ±3.21 GB |
| 58.5 GB | ±8.36 GB |

### 4.3 Cadans-aanname

De projectietabel is gebaseerd op de huidige L4 productiecadans:
- Timer: ±elke 5 minuten
- Theoretisch maximum: 288 snapshots/dag/pair
- Gemeten 48u audit: ~250-260 snapshots/dag/pair
- Projectie: ±750 MB/pair/maand raw

Storage schaalt lineair met:
- aantal pairs
- aantal snapshots per dag
- aantal timeframes per snapshot (altijd 5)
- raw_json grootte per timeframe

**Als cadence verandert, moet de storageprojectie opnieuw berekend worden.**

Gemeten ratio van 7.0x is één puntmeting op één DB. Herhaal bij grotere dataset.

## 5. Archive safety rules

**Nooit gzippen:** actieve maand, vorige maand, maand daarvoor.

**Alleen gzippen als:**
- buiten rolling 3-month window
- WAL checkpoint OK (zie §5.1)
- SQLite integrity_check OK
- geen actieve writer
- sha256 opgeslagen
- gzip integrity OK
- decompress test OK

### 5.1 WAL-mode regel

De L4 databases draaien in WAL-mode. Een `.sqlite`-bestand kan onvolledig zijn als er niet-gecheckpointe transacties in een naastliggend `.sqlite-wal` bestand staan.

**Verboden:** alleen de `.sqlite` gzippen zolang WAL/SHM-bestanden bestaan of checkpoint niet geverifieerd is.

**Verplicht vóór archiveren:**
1. Open een normale schrijfbare SQLite-connectie op het te archiveren `.sqlite`-bestand
2. Run `PRAGMA wal_checkpoint(TRUNCATE)`
3. Sluit de connectie netjes
4. Verifieer dat geen naastliggende bestanden bestaan:
   - `<YYYY-MM>.sqlite-wal`
   - `<YYYY-MM>.sqlite-shm`
5. Als `.sqlite-wal` of `.sqlite-shm` blijft bestaan: **STOP**, niet archiveren
6. Als writer actief is of checkpoint faalt: **STOP**, niet archiveren

`PRAGMA integrity_check` op alleen het `.sqlite`-bestand vangt dit probleem niet betrouwbaar, want een niet-gecheckpointe WAL kan ontbreken terwijl integrity_check toch OK zegt.

## 6. Archive stappen

1. Controleer dat bestand buiten rolling 3-month window valt
2. Controleer dat er geen actieve writer is
3. Run `PRAGMA wal_checkpoint(TRUNCATE)`
4. Verifieer dat geen `.sqlite-wal` en geen `.sqlite-shm` naast bestand bestaan
5. Run SQLite `PRAGMA integrity_check` op de `.sqlite`
6. Maak sha256 van originele `.sqlite`
7. Gzip naar `.sqlite.gz`
8. Run `gzip -t` op `.sqlite.gz`
9. Decompress naar `/tmp`
10. Run SQLite `PRAGMA integrity_check` op gedecomprimeerde kopie
11. Schrijf archive manifest
12. Verwijder originele `.sqlite` pas na alle checks
13. Verwijder nooit `.sqlite.gz` na restore-test

## 7. Manifest

Elke archive actie registreert:
- pair, original_file, archived_file
- original_size_bytes, gzip_size_bytes, compression_ratio
- original_sha256, archived_sha256
- archive_timestamp_utc
- sqlite_integrity_before, gzip_test_ok, decompress_integrity_ok
- removed_original_yes_no
- wal_checkpoint_ok
- wal_checkpoint_mode
- wal_file_absent_yes_no
- shm_file_absent_yes_no
- writer_check_ok
- cadence_assumption_snapshots_per_day
- compression_ratio_measured

Locatie: `projects/hermes-v03-interpreter/l4_store/archive_manifest.jsonl`

## 8. Restore contract

Restore: eerst decomprimeren → `/tmp` → read-only openen. Nooit productie overschrijven zonder expliciete opdracht. Originele `.gz` behouden.

### 8.1 Query gap waarschuwing

**BELANGRIJK — stille gaten:**

De huidige L4-querytools lezen alleen bestaande `.sqlite`-bestanden. Als een maand alleen als `.sqlite.gz` bestaat, wordt die maand niet automatisch gelezen.

**Gevolg:** Een historische query/backtest/outcome-analyse over een periode met gearchiveerde maanden kan stilzwijgend onvolledig zijn. Dat kan eruitzien als "geen data", terwijl de data alleen gecompressed is.

**Contractregel:** Elke analyse over een periode ouder dan de 3-month unzipped window vereist eerst expliciete restore/decompress van de betrokken maandbestanden naar een tijdelijke of afgesproken read-only locatie.

**Verboden:**
- Geen historische analyse over gzipped maanden zonder restore
- Geen silent skip accepteren als "geen data"
- Tools moeten later archive-aware worden of vooraf restored data gebruiken

## 9. Niet doen

- Geen dedup-fix
- Geen raw_hash wijziging
- Geen DB schema wijziging
- Geen L4 core wijziging
- Geen service/timer wijziging
- Geen Analyst/L5/Trader

## 10. Later

Mogelijke maandelijkse archive cronjob. Nu alleen contract, geen script, geen timer, geen gzip-actie zonder aparte opdracht.

## 11. Conclusie

3 maanden unzipped, oudere maanden veilig naar `.sqlite.gz` met WAL-check, query-gap waarschuwing en gedocumenteerde cadans-aanname. Dedup blijft ongewijzigd. Opschaling niet geblokkeerd.
