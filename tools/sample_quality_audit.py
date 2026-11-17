"""Standalone CSV data quality audit; outputs aggregates, never source rows."""
import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

REQUIRED = ("sample_id","sample_type","collection_date","status","storage_location","owner","temperature")

def audit_csv(path):
    counts=Counter()
    seen=set()
    rows=0
    with open(path,encoding="utf-8-sig",newline="") as handle:
        reader=csv.DictReader(handle)
        missing=set(REQUIRED)-set(reader.fieldnames or [])
        if missing:
            raise ValueError("Input missing required columns: "+", ".join(sorted(missing)))
        for row in reader:
            rows+=1
            if any(not (row.get(key) or "").strip() for key in REQUIRED):
                counts["missing_required_value"]+=1
            ident=(row.get("sample_id") or "").strip()
            if ident:
                if ident in seen:
                    counts["duplicate_sample_id"]+=1
                seen.add(ident)
            try:
                temperature=float(row["temperature"])
                if not -200 <= temperature <= 100:
                    counts["temperature_out_of_range"]+=1
            except (ValueError,TypeError):
                counts["invalid_temperature"]+=1
            try:
                date.fromisoformat((row.get("collection_date") or "").strip())
            except ValueError:
                counts["invalid_collection_date"]+=1
    return {"rows_scanned":rows,"unique_nonempty_ids":len(seen),
            "quality_flags":dict(sorted(counts.items())),
            "flagged_checks_total":sum(counts.values()),"has_quality_flags":bool(counts)}

def main():
    parser=argparse.ArgumentParser(description="Audit lab sample CSV quality")
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    report=audit_csv(args.input)
    Path(args.output).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Scanned {report['rows_scanned']} rows; detected {report['flagged_checks_total']} quality flags")

if __name__=="__main__":
    main()
