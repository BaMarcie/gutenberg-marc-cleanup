# MARC modification template: move place-name subjects from 650 to 651

**Template name:** `London England 650 to 651`

## Version 1 (exact match)
- Action: **Move** every field `650` to field `651`
- Condition: **if** field `650` subfield `a` **matches** `London (England)` (RegEx off)
- Result: corrected records whose subject is exactly `London (England)`. Did not touch `Hammersmith (London, England)` and similar.

## Version 2 (pattern, to widen the match)
- Same action
- Condition: **if** `650$a` **matches** `\((London, )?England\)$` with **RegEx ticked**
- Meaning: the heading ends with `(England)` or `(London, England)`
- Always preview on one record first (**Edit → Modify record using template**). Check that only the place heading moves to 651 and the other 650 fields stay.

## Observed behaviour
- With **Every** field 650 and a condition on `$a`, only the matching 650 moved. The other 650 fields in the record stayed. (Checked in the preview on record 11.)
- Job reports list every record the job ran on, including those where nothing changed.

## Limits
- Covers England only. Other places need their own patterns.
- It moves the whole field, with its subfields (such as `$x` and `$v`).
