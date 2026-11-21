# Koha import and export practice (local test catalogue)

Hands-on practice with bulk MARC import, bulk correction and export in **Koha**, run on a local test installation (Koha in a VirtualBox virtual machine, staff interface on `localhost:8080`). The data is 500 public-domain Project Gutenberg records (see the companion project `gutenberg-marc-cleanup`).

> Nothing here touches a production catalogue. No passwords or credentials are stored in this repository.

## What this shows
- Staging and importing MARC records (Tools → Stage MARC records for import)
- Checking a new batch against records already in the catalogue before importing, so as not to create duplicates
- Fixing a cataloguing error in bulk with a **MARC modification template** and **Batch record modification**
- Verifying changes in the MARC view, the modification log and the background-job report
- Exporting records (Tools → Export catalog data) and reading them back in MarcEdit

## Environment
- Koha: local test install (version: _add yours from the footer or About page_)
- Host: Windows; Koha runs inside a VirtualBox VM
- Tools on the host: MarcEdit (MarcMaker and MarcBreaker)

## Steps

### 1. Prepare the file (MarcEdit)
1. Compile the `.mrk` text file into binary MARC with **MARC Tools → MarcMaker**, Default Character Encoding **UTF8**.
2. Save with a full path, so the file's location is known. Result: `gutenberg-500.mrc` (500 records).

### 2. Stage the file (Koha)
1. **Tools → Stage MARC records for import**; choose the file.
2. Settings: Record type *Bibliographic*, encoding *UTF-8*, format *MARC*, matching rule *Do not look for matching records*, and a comment so the batch is recognisable.
3. Click **Stage for import** and wait for the background job to reach 100%.
4. Open **Manage staged records** to review the batch (500 records, status *Staged*, match type *No match*).

### 3. Check before importing
The staged batch was **Batch 2**. The batch list showed that **Batch 1** (same file name, imported earlier) already held 500 records. Importing Batch 2 would have created 500 duplicates, so it was **not** imported. Instead, one existing record was opened in the MARC view and compared with the staged version (see `docs/batch-comparison.md`).

### 4. Fix a tagging problem in bulk
Place names such as *London (England)* were tagged **650** (topical) but are geographic names and belong in **651**.
1. **Tools → Batch editing → MARC modification templates**: new template with one action (see `docs/template-settings.md`).
2. Test on one record with **Edit → Modify record using template** (preview first).
3. Apply to the matching records with **Edit → Batch edit records** from a catalogue search.
4. Check the job report under **Administration → Jobs**.

Results:
- Job #4: record 11 modified.
- Job #5: records 2, 11, 238, 241, 319 and 415 processed. Records with exactly `London (England)` were corrected (for example record 238). Record 241 kept `Hammersmith (London, England)` as 650, because the exact-match condition did not match it. This showed that an exact-match condition is too narrow for place names, and led to a pattern-based condition (see `docs/template-settings.md`).

### 5. Export and verify
1. **Tools → Export catalog data → Export bibliographic records**, a small record range, **Don't export items**, MARC output.
2. Move the `.mrc` to Windows and open it with **MarcBreaker** (UTF8) to get a readable `.mrk`.
3. Confirm the changes: record 2 shows `=651 \0$aLondon (England)$vJuvenile fiction`, and Koha's own `942` and `999` fields are present (see `samples/`).

## Findings
- **Always compare before importing.** The earlier import had better data than the new file (see `docs/batch-comparison.md`), so the right decision was not to import.
- **"Successfully modified" does not mean "changed".** A batch job reports every record it ran on, including those where the condition matched nothing.
- **Exact-match conditions are safe but narrow; patterns are broader but need a preview.**
- **Exports are a good verification tool.** Reading the exported MARC in MarcEdit confirmed the change independently of Koha's interface.

## Known remaining issues
- Some subject strings still use `$x` for places inside a heading (for example `Poor $x England $x London`); these should be `$z`.
- Place names in other countries need their own conditions, or a lookup against the authority file.
- Heading checks in MarcEdit (Validate Headings) are the way to find more.

## Screenshots to add (blur usernames)
`docs/` is a good place for: the staged batch list, the template action, the job report, and the MARC view before and after.

## Related
- `gutenberg-marc-cleanup`: the conversion from CSV to MARC and the heading validation
