# System Auditor Marking Rubric

## Overview

The project is marked out of 100:

| Part                         | Weight |
| ---------------------------- | ------ |
| Part 1: Command-line auditor | 65     |
| Part 2: Flask API and client | 35     |

- Part 1 carries more weight because it assesses the core course outcomes:
  inheritance, polymorphism, and separation of responsibilities.

- Part 2 assesses applying those classes behind an HTTP interface.

## How the Project Will Be Marked

Each criterion is assessed using the evidence in your code and tests. The
rubric describes the expected understanding, not one required implementation.
Different attribute names, helper methods, message wording, and code
organization are acceptable if the design idea is clear and the required public
interfaces still work.

Choose the level that best describes your work for each criterion. Your score
for that criterion is its points multiplied by the share shown below. For
example, a criterion worth 10 points at the Mostly level earns 8 points.

| Level        | Meaning                                                                       | Share of points |
| ------------ | ----------------------------------------------------------------------------- | --------------- |
| Demonstrated | The concept is applied correctly and consistently.                            | 100%            |
| Mostly       | The concept is clear, with minor errors or one inconsistency.                 | 80%             |
| Partial      | Some understanding is shown, but there are significant gaps.                  | 60%             |
| Not shown    | Missing, not working, or the concept is avoided (for example, by type tests). | 0%              |

All criteria are worth multiples of 5 points, so each level gives a
whole-number score.

### Marking Procedure

1. For the final project mark, review the completed Part 2 project. Use the
   `project_p01` tag and Git history to verify the Part 1 checkpoint.
1. Run `uv run python -m pytest` from the project folder.
1. Review `checks.py`, `audit.py`, `system_auditor_server.py`, and
   `audit_client.py`. These files show most of the assessed design. Check other
   files only when needed to confirm a criterion.
1. Review `git log --oneline` and `git tag -n` for the required project history
   and tags.

Passing tests are evidence, not the mark. A passing suite with poor design can
still lose design marks, and a well-designed solution with a minor test failure
can still earn most of the design marks.

## Part 1: Command-line Auditor (65)

| Criterion | Points | Evidence of understanding | Common signs of partial credit |
| --- | --- | --- | --- |
| 1. Inheritance and abstract parent | 15 | `SystemCheck` holds the shared state (requirement, description, name).<br>`SystemCheck` declares `measure()` as abstract.<br>Subclasses reuse parent initialization, typically with `super()`, instead of duplicating common setup. | Subclasses repeat parent attributes and setup.<br>`SystemCheck` can be created directly. |
| 2. Polymorphism and overriding | 15 | `run()` is defined once in `SystemCheck`.<br>`run()` calls `self.measure()` and compares the result.<br>Subclasses override `measure()` for resource-specific behavior.<br>`Audit.run()` calls `check.run()` without checking types. | `run()` is copied into each subclass.<br>`measure()` returns a pass/fail value.<br>`isinstance()` or `type` tests choose behavior. |
| 3. Separation of responsibilities | 10 | `CheckResult` stores one result.<br>`AuditReport` stores the overall outcome.<br>`Audit` builds and runs checks.<br>File access and printing are only in the CLI.<br>`Audit` (definition) and `AuditReport` (outcome) are kept separate. | Classes print or read files.<br>`passed` is computed outside `AuditReport`.<br>One class does most of the work. |
| 4. Object creation and validation | 5 | `create_check()` maps each specification to the correct class without measuring the computer.<br>`create_check()` rejects missing required keys and unknown check types.<br>`Audit` validates its required keys, non-empty ID and description, and checks list. | Check creation logic is duplicated in `Audit` instead of using `create_check()`.<br>Errors are printed or hidden instead of raised.<br>Creating an audit measures the computer. |
| 5. Command-line program and JSON | 5 | `main()` validates `sys.argv` and prints usage.<br>`main()` reads the definition and prints the report.<br>`main()` writes `to_dict()` as JSON when a filename is given.<br>Uses `if __name__ == "__main__":`. | No usage message.<br>JSON is built by hand instead of from `to_dict()`.<br>Errors are hidden with a broad `except`. |
| 6. Testing | 10 | `test_cpu_check` uses `fake_system`.<br>`test_cpu_check` creates the check through `create_check()`.<br>`test_cpu_check` asserts the type, requirement, description, and measurement.<br>Supplied tests pass and are unchanged. | CPU test is missing assertions.<br>CPU test measures the real computer.<br>Supplied tests were edited to pass. |
| 7. Code quality and Git process | 5 | Google-style docstrings.<br>Readable names and type hints where helpful.<br>A commit for each build step.<br>Annotated `project_p01` tag. | Few commits.<br>Missing tag.<br>Missing or placeholder docstrings. |

## Part 2: Flask API and Client (35)

| Criterion | Points | Evidence of understanding | Common signs of partial credit |
| --- | --- | --- | --- |
| 8. Flask API reusing Part 1 | 10 | `GET /api/status` and `POST /api/audit` work.<br>The audit route creates a new `Audit` from the request JSON.<br>The audit route runs the audit and returns `to_dict()`.<br>Part 1 classes are unchanged.<br>The server does not repeat audit logic. | Audit logic is rewritten in the route.<br>Part 1 classes are modified for HTTP.<br>Wrong method or route. |
| 9. Status codes and error handling | 5 | 200 for both passed and failed audits.<br>400 for non-JSON or invalid definitions.<br>500 for measurement errors.<br>The `try` block for measurement errors covers only `audit.run()`.<br>The client separates connection errors from HTTP errors.<br>The client continues with the remaining hosts after an error. | Failed audits return 4xx.<br>One broad `try` around the whole view.<br>One host error stops the client. |
| 10. HTTP client design | 10 | `AuditClient` stores one host.<br>Sends the definition with a timeout and calls `raise_for_status()`.<br>Returns a consistent host result and copies `passed` from the server instead of comparing measurements.<br>`main()` displays host results and writes them to JSON in hosts-file order.<br>`main()` handles incorrect argument counts with a usage message.<br>File access and printing stay in `main()`. | Client recalculates PASS/FAIL.<br>Result fields differ by case.<br>Results are not displayed or saved as required.<br>`AuditClient` prints or reads files. |
| 11. Testing the server and client | 5 | Server fixtures use `create_app()`, the Flask test client, and `fake_system`.<br>Server tests check status codes and response bodies.<br>Client tests replace `httpx.post` and do not use the network.<br>Client tests check the request, returned results, and saved output. | Tests start a real server or use the network.<br>Only status codes are checked.<br>Skeleton `pytest.fail()` markers remain. |
| 12. Project layout and Git process | 5 | Tests are moved to `tests`.<br>`pyproject.toml` has the pytest settings and dependencies, and `uv.lock` is updated.<br>`hosts.json` is valid and `.vscode/launch.json` includes the Part 2 launch configurations.<br>Commits follow each functionality addition.<br>Annotated `project_p02` tag is present without moving `project_p01`. | Duplicate pytest sections.<br>Tests left in the project folder.<br>Missing or outdated lockfile or launch configurations.<br>Missing tag or a single final commit. |

