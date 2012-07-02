import argparse
import json
import sys

from .core import parse_line, summarize


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize simplified five-field logs as JSON.")
    parser.add_argument("path", nargs="?", default="-", help="UTF-8 file or - for stdin")
    parser.add_argument("--strict", action="store_true", help="Fail on the first malformed nonblank line")
    parser.add_argument("--check-fixtures", metavar="JSONL")
    args = parser.parse_args(argv)
    try:
        if args.check_fixtures:
            if args.path != "-" or args.strict:
                parser.error("Use --check-fixtures alone")
            from .fixture_check import check
            print("Verified {} synthetic fixtures.".format(check(args.check_fixtures, parse_line)))
        else:
            if args.path == "-":
                result = summarize(sys.stdin, args.strict)
            else:
                with open(args.path, encoding="utf-8") as handle:
                    result = summarize(handle, args.strict)
            print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0
    except ValueError as error:
        print("error: " + str(error), file=sys.stderr)
        return 2
    except OSError as error:
        print("error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
