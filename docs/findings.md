# Findings

## 1. Structure validation (MarcEdit MARC Validator)
- 500 records checked: **no structural errors** reported.
- Duplicate check flagged one title, "Runoelmia". It is two different books (Gutenberg #20227 by Heinrich Heine and #20422 by Johann Wolfgang von Goethe, both Finnish translations), not a duplicate record. No record ID is repeated.
- Lesson: a duplicate check proposes candidates, and a cataloguer decides.

## 2. Heading validation (MarcEdit Validate Headings)
| Run | Subject headings found | Not found | Variants | Records flagged |
|---|---|---|---|---|
| 1. Names and full subject strings | 674 (6xx) | 362 (6xx) | 9 (6xx) | 328 of 500 |
| 2. Subject main term only (`$a`) | 800 | 236 | 9 | 182 of 500 |

Names in run 1: 343 found, 140 not found, 10 variants (1xx); 92 found, 49 not found, 1 variant (7xx).

Reading the results:
- Checking only the main term found 126 more headings, so a large share of run 1's "not found" came from subdivisions and my subfield coding. The same 9 subject variants appear in both runs, so they are the clearest corrections.
- "Not found" is not the same as "wrong": many 19th-century authors are not in the name authority file, and long subdivided strings are often valid without being individually established.

## 3. Manual check of one flagged record (Gutenberg #20071, "Sue, a little heroine")
Checked each 650 on id.loc.gov:

| Heading | Result | ID |
|---|---|---|
| Christian life | Approved LCSH | sh85025095 |
| London (England) | Found in the **Name Authority File** (geographic), not LCSH | n79005665 |
| Children with disabilities | Approved LCSH | sh85058689 |
| Thieves | Approved LCSH | sh85134855 |
| Poor children | Approved LCSH | sh85104852 |
| Child labor | Approved LCSH | sh85023444 |
| Abduction | Approved LCSH; scope note limits it to the kidnapping of women, so fit is worth reviewing (broader term: Kidnapping) | sh85000114 |

**Correction:** the place name London (England) is a geographic name from the Name Authority File and should be tagged **651**, not 650. This explains why the record was flagged. Fixed in MarcEdit with Find and Replace (`=650  \0$aLondon (England)` to `=651  \0$aLondon (England)`).

A second example from record #20074: "Cambrian Railway" is a corporate body and is a candidate for a 610 name heading rather than a 650 topical heading (not verified in the authority file).

## 4. When to use MarcEdit and when to use Python
- MarcEdit: quick, visual batch edits, validation, and authority checks on MARC files.
- Python: repeatable pipelines and unusual transformations, such as converting the CSV to MARC in `scripts/csv_to_mrk.py`.
