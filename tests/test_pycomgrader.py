import subprocess
import time
import unittest
from pathlib import Path

try:
    from pycomgrader import Grader, GraderError, Status
except ImportError:
    from src.pycomgrader import Grader, GraderError, Status


class TestGrader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.source_file = Path("tests/test_programs/test_program.cpp")
        cls.exec_file = Path("tests/test_programs/test_program.o")
        cls.test_cases_dir = Path("tests/test_cases")
        cls.grader = Grader(
            source_file=cls.source_file, time_limit=1000, memory_limit=32
        )
        if not cls.exec_file.exists():
            cls._compile_source_file()

    @classmethod
    def tearDownClass(cls):
        if cls.exec_file.exists():
            cls.exec_file.unlink()
        for tmp_file in Path("tests/test_programs").glob("*.tmp"):
            tmp_file.unlink()

    @classmethod
    def _compile_source_file(cls):
        subprocess.run(
            ["g++", cls.source_file, "-o", cls.exec_file],
            check=True,
        )

    def test_grade(self):
        results = self.grader.grade(self.test_cases_dir)
        expected_statuses = [Status.AC, Status.WA, Status.TLE]

        for result, expected_status in zip(results, expected_statuses):
            self.assertEqual(result.status, expected_status)

    def test_check_test_case(self):
        test_cases = [
            (
                "tests/test_cases/01.in",
                "tests/test_cases/01.out",
                Status.AC,
                "test accepted",
            ),
            (
                "tests/test_cases/02.in",
                "tests/test_cases/02.out",
                Status.WA,
                "test wrong answer",
            ),
            (
                "tests/test_cases/03.in",
                "tests/test_cases/03.out",
                Status.TLE,
                "test time limit exceeded",
            ),
        ]

        for input_file, output_file, expected_status, subtest_name in test_cases:
            with self.subTest(subtest_name):
                result = self.grader.check_test_case(input_file, output_file)
                self.assertEqual(result.status, expected_status)

    def test_init_with_source_file(self):
        grader = Grader(source_file=self.source_file, time_limit=1000, memory_limit=32)
        self.assertEqual(grader.source_file, self.source_file)
        self.assertIsNone(grader.exec_file)

    def test_init_with_exec_file(self):
        grader = Grader(exec_file=self.exec_file, time_limit=1000, memory_limit=32)
        self.assertEqual(grader.exec_file, self.exec_file)
        self.assertIsNone(grader.source_file)

    def test_init_with_both_files_raises_error(self):
        with self.assertRaises(GraderError):
            Grader(source_file=self.source_file, exec_file=self.exec_file)

    def test_init_with_no_files_raises_error(self):
        with self.assertRaises(GraderError):
            Grader()

    def test_valid_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            self.grader.source_file = Path("non_existent_file.cpp")

    def test_valid_dir_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            self.grader.grade("non_existent_dir")

    def test_monitor_process_time_limit_exceeded(self):
        with subprocess.Popen(["sleep", "10"]) as process:
            start = time.perf_counter()
            status, _ = self.grader._monitor_process(process, start, 0)
            self.assertEqual(status, Status.TLE)
            process.terminate()
            process.wait()

    def test_monitor_process_memory_limit_exceeded(self):
        with subprocess.Popen(
            ["python", "-c", "a = ' ' * 1024**3"]
        ) as process:  # Allocate 1GB
            start = time.perf_counter()
            status, _ = self.grader._monitor_process(process, start, 0)
            self.assertEqual(status, Status.MLE)
            process.terminate()
            process.wait()

    def test_monitor_process_runtime_error(self):
        with subprocess.Popen(["python", "-c", "import sys; sys.exit(1)"]) as process:
            start = time.perf_counter()
            status, _ = self.grader._monitor_process(process, start, 0)
            self.assertEqual(status, Status.RTE)
            process.terminate()
            process.wait()


if __name__ == "__main__":
    unittest.main()
