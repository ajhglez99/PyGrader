import argparse
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    from pycomgrader import cli_grader
except ImportError:
    from src.pycomgrader import cli_grader


class TestCLIGrader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.source_file = Path("tests/test_programs/test_program.cpp")
        cls.exec_file = Path("tests/test_programs/test_program.o")
        cls.test_cases_dir = Path("tests/test_cases")

    @classmethod
    def tearDownClass(cls):
        if cls.exec_file.exists():
            cls.exec_file.unlink()
        for tmp_file in Path("tests/test_programs").glob("*.tmp"):
            tmp_file.unlink()

    def _run_cli_grader_with_args(self, args, expected_exception, expected_code=None):
        sys.argv = args
        with self.assertRaises(expected_exception) as cm:
            cli_grader.run_cli_grader()
        if expected_code is not None:
            self.assertEqual(cm.exception.code, expected_code)

    def test_invalid_file_argument(self):
        self._run_cli_grader_with_args(
            ["pycomgrader", "invalid_file.cpp", str(self.test_cases_dir), "1000", "32"],
            argparse.ArgumentTypeError,
        )

    def test_invalid_directory_argument(self):
        self._run_cli_grader_with_args(
            ["pycomgrader", str(self.source_file), "invalid_directory", "1000", "32"],
            argparse.ArgumentTypeError,
        )

    def test_invalid_time_argument(self):
        self._run_cli_grader_with_args(
            [
                "pycomgrader",
                str(self.source_file),
                str(self.test_cases_dir),
                "invalid_time",
                "32",
            ],
            SystemExit,
            expected_code=2,
        )

    def test_invalid_memory_argument(self):
        self._run_cli_grader_with_args(
            [
                "pycomgrader",
                str(self.source_file),
                str(self.test_cases_dir),
                "1000",
                "invalid_memory",
            ],
            SystemExit,
            expected_code=2,
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_results_printed_properly(self, mock_stdout):
        sys.argv = [
            "pycomgrader",
            str(self.source_file),
            str(self.test_cases_dir),
            "1000",
            "32",
        ]
        try:
            cli_grader.run_cli_grader()
        except SystemExit:
            pass
        output = mock_stdout.getvalue()
        self.assertIn("final score:", output)


if __name__ == "__main__":
    unittest.main()
