"""Pytest Scorer

This module runs pytest tests and generates a score report compatible with
the GitHub Classroom autograding-grading-reporter action.

It runs the specified test files and optionally the specific tests.
Each test counts for one point.

It also creates a score equal to the number of passed tests
"""

import argparse
import enum
import json
import os
import pathlib
import sys

import pytest


class GraderResult(enum.Enum):
    """Overall grading status results for use by autograding-grading-reporter

    Pytest and classroom-resources/autograding-grading-reporter use different strings
    these are autograding-grader form
    """

    PASS = "pass"
    FAIL = "fail"


class PytestResult(enum.Enum):
    """Pytest test outcome results.

    Pytest and classroom-resources/autograding-grading-reporter use different strings
    these are the pytest output form
    """

    PASSED = "passed"
    FAILED = "failed"


class ResultsCollector:
    """Collects pytest test results for scoring.

    Based on:
        https://stackoverflow.com/a/72278485  Posted by hoefling
        Retrieved: 2026-02-04
        License - CC BY-SA 4.0

    Attributes:
        reports_dict: Dictionary mapping test node IDs to TestReport objects.

    References:
        - https://docs.pytest.org/en/stable/reference/reference.html#pytest-hookimpl
        - https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html#writinghooks

    """

    def __init__(self):
        """Initialize the ResultsCollector with an empty reports dictionary."""
        self.test_reports = {}

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Pytest hook to capture test results.

        Args:
            item: The test item being executed.
            call: The call phase of the test.

        Yields:
            The outcome of the test execution.
        """
        outcome = yield

        # report is a pytest TestReport
        # https://docs.pytest.org/en/stable/reference/reference.html#testreport
        report = outcome.get_result()

        if report.when == "call":
            self.test_reports[report.nodeid] = report


def score_tests(test_files: list[pathlib.Path], tests: list[str]):
    """Run pytest tests and generate a score with each passed test counting as
    a score of 1.

    Executes tests from the specified test files and calculates a score based on
    the number of passed tests. If specific tests are provided, only those tests
    are graded; otherwise, all collected tests from the files are graded.
    Output the results in a format compatible with autograding-grading-reporter
    GitHub Action.

    Args:
        test_files: List of paths to pytest test files to run.
        tests: List of specific test node IDs to grade (e.g.,
            'test_file.py::test_name'). If empty or None, all collected
            tests will be graded.

    Returns:
        int: 0 if all tests passed, 1 otherwise.
    """
    total_score = 0
    collector = ResultsCollector()

    # Run pytest to collect and execute tests
    pytest_args = ["-p", "no:terminal"] + test_files
    pytest.main(
        args=pytest_args,
        plugins=[collector],
    )

    # Get all test IDs from the collector
    collected_test_ids = sorted(collector.test_reports.keys())

    # if the tests to score are not specified use all collected tests from files
    if not tests or len(tests) == 0:
        tests = collected_test_ids

    max_score = len(tests)

    test_results = []

    for test_nodeid in tests:
        test_report = collector.test_reports.get(test_nodeid)

        if test_report and test_report.outcome == PytestResult.PASSED.value:
            test_status = GraderResult.PASS.value
            test_score = 1
            total_score += 1
        else:
            test_status = GraderResult.FAIL.value
            test_score = 0

        test_results.append(
            {
                "name": test_nodeid,
                "status": test_status,
                "score": test_score,
                "max_score": 1,
            }
        )

    # Output for GitHub Actions
    # classroom-resources/autograding-grading-reporter
    results = {
        "tests": test_results,
    }

    # Check if running in gitub action
    if os.environ.get("GITHUB_ACTIONS"):
        json_output = json.dumps(results, ensure_ascii=True, separators=(",", ":"))
        with open(
            os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8", newline="\n"
        ) as f:
            f.write(f"results={json_output}\n")

    # Write to Results terminal
    print("\nResults:")
    print(f"{json.dumps(results, indent=4)}")
    print(f"\nScore: {total_score}/{max_score}")

    # Exit with non-zero if not all tests passed
    if total_score != max_score:
        return 1
    else:
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run specific pytest tests and generate autograding results"
    )
    parser.add_argument(
        "test_files",
        nargs="+",
        help="One or more pytest test files to run",
    )
    parser.add_argument(
        "-t",
        "--tests",
        nargs="+",
        required=True,
        help="Specific test node IDs to grade (e.g., test_file.py::test_name)",
    )

    args = parser.parse_args()
    sys.exit(score_tests(args.test_files, args.tests))
