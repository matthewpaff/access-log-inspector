from pathlib import Path
import unittest

from access_log_lab.core import parse_line, summarize
from access_log_lab.fixture_check import check


class LogTests(unittest.TestCase):
    def test_parses_boundary_status_and_duration(self):
        row = parse_line("2013-01-01T00:00:00+00:00 GET / 599 3600000")
        self.assertEqual((row["status"], row["duration_ms"]), (599, 3600000))

    def test_rejects_naive_dates_and_invalid_fields(self):
        for line in ("2013-01-01T00:00:00 GET / 200 10", "2013-01-01T00:00:00Z GET / 099 1",
                     "2013-01-01T00:00:00Z GET / 200 3600001", "2013-01-01T00:00:00Z GET / 200 1.2"):
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_line(line)

    def test_aggregation_and_malformed_policy(self):
        lines = ["2013-01-01T00:00:00Z GET /a 200 10", "bad", "\n",
                 "2013-01-01T00:00:00Z POST /a 503 20", "2013-01-01T00:00:00Z GET /b 200 30"]
        result = summarize(lines)
        self.assertEqual((result["requests"], result["malformed"], result["server_errors"], result["average_ms"]), (3, 1, 1, 20.0))
        self.assertEqual(result["top_paths"][0], {"path": "/a", "count": 2})
        with self.assertRaisesRegex(ValueError, "Line 2"):
            summarize(lines, strict=True)

    def test_empty_input(self):
        self.assertIsNone(summarize([])["average_ms"])

    def test_all_generated_fixtures(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures" / "cases.jsonl", parse_line), 350)


if __name__ == "__main__":
    unittest.main()
