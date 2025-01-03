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

    FINAL_SCORE_STRING = "final score:"
    COMPILE_ERROR_STRING = "compile error"

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
        with patch.object(sys, "argv", args):
            with self.assertRaises(expected_exception) as context_manager:
                cli_grader.run_cli_grader()
            if expected_code is not None:
                self.assertEqual(context_manager.exception.code, expected_code)

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

    def test_results_printed_properly(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch.object(
                sys,
                "argv",
                [
                    "pycomgrader",
                    str(self.source_file),
                    str(self.test_cases_dir),
                    "1000",
                    "32",
                ],
            ):
                cli_grader.run_cli_grader()
                output = mock_stdout.getvalue()
                self.assertIn(self.FINAL_SCORE_STRING, output)

    def test_compile_error(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch.object(
                sys,
                "argv",
                [
                    "pycomgrader",
                    "tests/test_programs/compile_error_program.cpp",
                    str(self.test_cases_dir),
                    "1000",
                    "32",
                ],
            ):
                cli_grader.run_cli_grader()
                output = mock_stdout.getvalue()
                self.assertIn(self.COMPILE_ERROR_STRING, output)


if __name__ == "__main__":
    unittest.main()
