import unittest

from pygrader.pygrader import Grader, GraderError, Status


class PyGraderTest(unittest.TestCase):
    def test_ac_submission(self):
        grader = Grader(source_file="tests/submits/atoi_ok.cpp")
        results = grader.grade("tests/testcases")

        for result in results:
            self.assertEqual(result.status, Status.AC)

    def test_wa_submission(self):
        grader = Grader(source_file="tests/submits/atoi_wa.cpp")

        with self.subTest("test wrong answer"):
            result = grader.check_test_case(
                "tests/testcases/02.in", "tests/testcases/02.out"
            )
            self.assertEqual(result.status, Status.WA)

        with self.subTest("test time limit exceeded"):
            result = grader.check_test_case(
                "tests/testcases/15.in", "tests/testcases/15.out"
            )
            self.assertEqual(result.status, Status.TLE)

        with self.subTest("test runtime error"):
            result = grader.check_test_case(
                "tests/testcases/14.in", "tests/testcases/14.out"
            )
            self.assertEqual(result.status, Status.RTE)

    def test_raises_error(self):
        with self.assertRaises(GraderError):
            Grader()

        with self.assertRaises(GraderError):
            Grader(
                source_file="tests/submits/atoi_wa.cpp",
                exec_file="tests/submits/atoi_wa.o",
            )

        with self.assertRaises(TypeError):
            Grader(source_file="asd*<>")

        with self.assertRaises(TypeError):
            grader = Grader(source_file="tests/submits/atoi_ac.cpp")
            grader.check_test_case("tests/testcases/01.in", "asd*<>")

        with self.assertRaises(GraderError):
            grader = Grader(source_file="tests/submits/atoi_ce.cpp")
            grader.check_test_case("tests/testcases/01.in", "tests/testcases/01.out")

    def test_changing_file_attributtes(self):
        grader = Grader(source_file="tests/submits/atoi_ok.cpp")
        with self.subTest("Compile flag is false when source_file is initialized"):
            self.assertFalse(grader._compiled)

        with self.subTest("Compile flag is true when source_file is initialized"):
            grader.exec_file = "tests/submits/atoi_wa.o"
            self.assertTrue(grader._compiled)

        with self.subTest("source_file is set to None if exec_file is initialized"):
            self.assertIsNone(grader.source_file)


if __name__ == "__main__":
    unittest.main()
