# Access Log Lab

Summarize a deliberately simplified log format as JSON: timestamp method path status duration_ms.

This original small project uses **Python 3.10+ and only its standard library**.
No packages, virtual environment, service, or network access are required.

## Run

From this repository directory:

```console
python access_log.py --help
python access_log.py examples/sample.log
python access_log.py examples/sample.log --strict
python access_log.py --check-fixtures fixtures/cases.jsonl
python -m unittest discover -s tests -v
```

This is not an Apache or Nginx parser. Timestamps require an ISO time and timezone; status is 100–599, duration is integer milliseconds from 0 to 3600000. Blank lines are ignored. Malformed lines are counted and skipped, or cause an input error in strict mode. Summaries include status counts, server errors, mean duration, and the ten most common paths.

Output is JSON (or a fixture-check summary). Exit codes are 0 for success,
1 for file failures, and 2 for invalid input. Errors go to stderr.
For file-based tools, `-` reads stdin. Use UTF-8 input files.

## Structure and branches

- `access_log_lab/core.py`: pure parsing or analysis logic.
- `access_log_lab/cli.py`: command arguments and file input/output.
- `access_log_lab/generate_fixtures.py`: deterministic original sample cases.
- `access_log_lab/fixture_check.py`: expected-result/error validation.
- `fixtures/cases.jsonl`: 367 synthetic cases, one added per artificial dated commit.
- `tests/`: independently chosen boundary cases plus corpus validation.

`feature/core` and `feature/cli` retain the corresponding development snapshots.
`data/synthetic-fixtures` marks the completed corpus; `docs/usage` and `main` contain
the final documentation and tests. There are no copied upstream commits.

## Generate examples

```console
python generate_fixtures.py --count 20
```

This prints reproducible JSONL and **does not create or date Git commits**. The
historical-looking Git timeline is a separate, documented simulation. Many cases
vary generated values; they do not imply separate design decisions or features.

Keep contributions focused, add a regression test for changed behavior, and run
the standard-library tests. Never add real private data or credentials. Record
actual dates for new work. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
