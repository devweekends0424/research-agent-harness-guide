"""Pure offline tests of aggregate traffic merging."""

import unittest

from scripts.archive_traffic import merge_daily


class TrafficTests(unittest.TestCase):
    def test_merge_and_update_without_duplicates(self):
        views = {"views": [{"timestamp": "2026-11-07T00:00:00Z", "count": 10, "uniques": 4}]}
        clones = {"clones": [{"timestamp": "2026-11-07T00:00:00Z", "count": 2, "uniques": 1}]}
        result = merge_daily({}, views, clones)
        self.assertEqual(result["daily"]["2026-11-07"]["views"]["count"], 10)
        self.assertEqual(result["daily"]["2026-11-07"]["clones"]["uniques"], 1)
        again = merge_daily(result, views, clones)
        self.assertEqual(len(again["daily"]), 1)

    def test_preserve_old_dates(self):
        old = {"daily": {"2026-10-01": {"views": {"count": 1, "uniques": 1}}}}
        merged = merge_daily(old, {"views": []}, {"clones": []})
        self.assertIn("2026-10-01", merged["daily"])


if __name__ == "__main__":
    unittest.main()
