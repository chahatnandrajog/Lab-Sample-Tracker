import csv
import tempfile
import unittest
from pathlib import Path
from tools.sample_quality_audit import audit_csv, REQUIRED

BASE=["A1","blood","2026-11-01","received","freezer","technician","-20"]

class SampleAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"samples.csv"

    def write(self,rows,fields=REQUIRED):
        with self.path.open("w",newline="",encoding="utf-8") as handle:
            writer=csv.writer(handle)
            writer.writerow(fields)
            writer.writerows(rows)

    def test_valid(self):
        self.write([BASE])
        self.assertEqual(audit_csv(self.path)["flagged_checks_total"],0)

    def test_duplicate(self):
        self.write([BASE,BASE])
        self.assertEqual(audit_csv(self.path)["quality_flags"]["duplicate_sample_id"],1)

    def test_missing(self):
        self.write([["",*BASE[1:]]])
        self.assertEqual(audit_csv(self.path)["quality_flags"]["missing_required_value"],1)

    def test_out_of_range_temperature(self):
        self.write([BASE[:-1]+["101"]])
        self.assertEqual(audit_csv(self.path)["quality_flags"]["temperature_out_of_range"],1)

    def test_invalid_temperature(self):
        self.write([BASE[:-1]+["oops"]])
        self.assertEqual(audit_csv(self.path)["quality_flags"]["invalid_temperature"],1)

    def test_invalid_date(self):
        self.write([BASE[:2]+["2026-02-30"]+BASE[3:]])
        self.assertEqual(audit_csv(self.path)["quality_flags"]["invalid_collection_date"],1)

    def test_missing_header(self):
        self.write([],REQUIRED[:-1])
        with self.assertRaisesRegex(ValueError,"missing required columns"):
            audit_csv(self.path)

    def test_source_rows_not_exposed(self):
        self.write([BASE])
        self.assertNotIn("A1",str(audit_csv(self.path)))

if __name__=="__main__":
    unittest.main()
