# Lab sample CSV quality audit

Standalone offline pre-import auditing tool for the Lab Sample Tracker project.

Checks required columns, missing values, duplicate sample IDs, ISO calendar dates, and numeric temperatures in the range -200 to 100 Celsius. Outputs aggregate quality indicators in JSON without exposing original sample records. Uses only Python standard library; does not call the external AI service.

Run from repository root:

```bash
python tools/sample_quality_audit.py --input samples.csv --output quality_report.json
python -m unittest discover -s tests -p 'test_sample_quality_audit.py' -v
```

The report contains rows scanned, count of unique non-empty IDs, per-category flag counts, and combined flag count. A record may produce multiple flags. This tool audits raw CSVs independently of the web application's import endpoint. It does not modify the database.
