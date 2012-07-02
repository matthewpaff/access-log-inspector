"""Original synthetic parser cases. No real IP addresses or traffic records."""
import argparse
import json


def make_case(index):
    label = "synthetic-log-{:04d}".format(index)
    stamp = "2013-{:02d}-{:02d}T{:02d}:{:02d}:00Z".format(1 + index % 12, 1 + index % 28, index % 24, index % 60)
    method = ("GET", "POST", "PUT", "DELETE", "HEAD")[index % 5]
    path = "/sample/{}/item/{}".format(index % 7, index)
    status = (200, 201, 204, 301, 400, 404, 429, 500, 503)[index % 9]
    duration = (index * 37) % 4000
    parts = [stamp, method, path, str(status), str(duration)]
    kind = index % 11
    replacements = {0: (3, "999"), 1: (4, "-2"), 2: (1, "get"),
                    3: (0, "not-a-date"), 4: (2, "not-a-path")}
    if kind in replacements:
        position, value = replacements[kind]
        parts[position] = value
        return {"id": label, "input": " ".join(parts), "expected_error": True}
    if kind == 5:
        return {"id": label, "input": " ".join(parts) + " extra-field", "expected_error": True}
    return {"id": label, "input": " ".join(parts), "expected": {
        "timestamp": stamp, "method": method, "path": path, "status": status, "duration_ms": duration}}


def main():
    parser = argparse.ArgumentParser(description="Print synthetic parser cases as JSONL.")
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.count <= 10000:
        parser.error("Count must be between 1 and 10000")
    for index in range(args.count):
        print(json.dumps(make_case(index), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
