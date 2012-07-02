"""Summarize a deliberately simple five-field log format, not Apache/Nginx logs."""
from collections import Counter
from datetime import datetime
import re

METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}


def parse_line(line):
    if not isinstance(line, str):
        raise ValueError("Log line must be text")
    parts = line.split()
    if len(parts) != 5:
        raise ValueError("Expected timestamp method path status duration_ms")
    stamp, method, path, status, duration = parts
    try:
        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Invalid ISO timestamp") from None
    if parsed.tzinfo is None or "T" not in stamp:
        raise ValueError("Timestamp must include time and timezone")
    if method not in METHODS or not path.startswith("/"):
        raise ValueError("Use a supported uppercase method and a path starting with /")
    if not re.fullmatch(r"[1-5][0-9]{2}", status):
        raise ValueError("Status must be 100–599")
    if not re.fullmatch(r"[0-9]{1,7}", duration) or int(duration) > 3600000:
        raise ValueError("Duration must be integer milliseconds from 0 to 3600000")
    return {"timestamp": stamp, "method": method, "path": path,
            "status": int(status), "duration_ms": int(duration)}


def summarize(lines, strict=False):
    rows, malformed = [], 0
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            rows.append(parse_line(line))
        except ValueError as error:
            if strict:
                raise ValueError("Line {}: {}".format(number, error)) from error
            malformed += 1
    count = len(rows)
    return {"requests": count, "malformed": malformed,
            "server_errors": sum(row["status"] >= 500 for row in rows),
            "average_ms": round(sum(row["duration_ms"] for row in rows) / count, 2) if count else None,
            "status_counts": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
            "top_paths": [{"path": path, "count": count} for path, count in sorted(
                Counter(row["path"] for row in rows).items(), key=lambda item: (-item[1], item[0]))[:10]]}
