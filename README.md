# Gutenberg MARC Cleanup: converting and validating 500 catalogue records

A practice project in library metadata work. I took 500 Project Gutenberg records in Dublin Core (CSV), converted them to MARC 21, and used **MarcEdit** and the Library of Congress **id.loc.gov** service to validate the structure and check the subject and name headings against authority files.

## What this shows
- Crosswalking Dublin Core to MARC 21 (RDA fields 336/337/338, 041, 100/245/650/700, 856)
- Validating records with MarcEdit's MARC Validator and Validate Headings tools
- Checking headings against LCSH and the LC Name Authority File by hand
- Finding and correcting tagging errors (for example, a place name tagged 650 instead of 651)
- Writing a script (Python) for repeatable conversion, and knowing when MarcEdit is the better tool

## Repository contents
| Path | What it is |
|---|---|
| `data/gutenberg-clean-500.csv` | Source: 500 Gutenberg records (Dublin Core columns) |
| `data/gutenberg_500.mrk` | Converted records in MarcEdit text format (open in MarcEdit, or compile to .mrc with MarcMaker) |
| `scripts/csv_to_mrk.py` | The conversion script (Python 3, standard library only) |
| `docs/findings.md` | Validation results, what the numbers mean, and corrections found |
[`koha-import-export/`](koha-import-export/) Practice with bulk import, correction and export in Koha (local test catalogue) |

## How to reproduce
```
python scripts/csv_to_mrk.py data/gutenberg-clean-500.csv data/gutenberg_500.mrk
```
Then in MarcEdit: **Edit Records** → open the `.mrk` file → run the validator (Tools) and **Validate Headings** (Reports).

## Known limitations (deliberate, for a practice dataset)
- Place names are tagged 650; geographic headings belong in **651**.
- Subdivisions are guessed: known forms such as "Fiction" go in `$v`, everything else in `$x`; places inside a heading should be `$z`.
- Personal names have no `$q` (fuller form).
- The 500 note records when a book was added to Gutenberg, not its publication date.
- Subjects come from Gutenberg and are not re-evaluated for fit.

## Sources and tools
- Project Gutenberg catalogue metadata (https://www.gutenberg.org)
- MarcEdit (Terry Reese)
- Library of Congress Linked Data Service, LCSH and Name Authority File (https://id.loc.gov)

Author: Brighton Tizirai, Discovery and Metadata Librarian
