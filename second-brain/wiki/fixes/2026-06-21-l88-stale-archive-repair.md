2026-06-21 — L88 stale archive repair

Probleem: ohlc_archive/ bevatte stale/partiale 240m candles voor 3 periodes (22-24 mei, 25-30 mei deels, 31 mei-3 jun). L88 auto mode gaf archive prioriteit boven cache, waardoor chart platte candles toonde.

Fix:
1. `tools/repair_stale_ohlc_archive.py` — herschreven via inspectie OHLC/range vergelijking archive vs cache
2. 126 candles vervangen over 6 pairs (112 + 14 na detectie-fix)
3. 672/672 archive-cache timestamps matchen na repair
4. Source guard in L0_data auto mode: detecteert stale door range vergelijking, geeft cache voorrang
5. Backup in backups/ohlc_archive_repair_20260621*, backups/L0_data_original_20260621.py

Bestanden:
- tools/repair_stale_ohlc_archive.py
- layer88_historical_audit/L0_data.py (aangepast)
- charts/full/files/audit_l88_date_specific_candle_truth.md (audit)
- charts/full/files/fix_l88_stale_archive_source_switch.md (fixrapport)
- charts/full/files/repair_stale_ohlc_archive_{dryrun,apply}.{csv,json,md} (bewijs)

Geen commit. Geen data verwijderd.
