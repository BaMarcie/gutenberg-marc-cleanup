# Batch 1 (existing, imported) vs Batch 2 (new file): record for "Little Pollie" (Gutenberg #20080)

| Field | Existing record in Koha (Batch 1) | New file (Batch 2) |
|---|---|---|
| 001 | `PG20080` | `gutenberg20080` |
| 040 | `$b eng $c GZU` (local institution) | none |
| 500 | `Project Gutenberg release date: 2006-12-10.` | `Added to Project Gutenberg 2006-12-10.` |
| Century subdivision | `$y 19th century` (chronological) | `$x 19th century` (topical) |
| 856 | has `$y Read online at Project Gutenberg` | link only, no display text |
| 942 / 999 | present (added by Koha at import) | not present until imported |

Both versions had the same two issues: places inside a subject string coded `$x` instead of `$z`, and *London (England)* tagged 650 instead of 651.

**Decision:** keep the existing records and do not import Batch 2, to avoid 500 duplicates of weaker records. The comparison fed back into the conversion script's improvement list (040 source field, `$y` for centuries, 856 `$y` text, clearer 500 wording).
