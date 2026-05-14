#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RULE = ROOT / "rule-set" / "claude-full.json"

EXPECTED = {
    "domain_suffix": {
        "anthropic.com",
        "claude.ai",
        "claude.com",
        "clau.de",
        "claudemcpclient.com",
        "claudemcpcontent.com",
        "claudeusercontent.com",
        "sentry.io",
        "statsigapi.net",
        "intercom.io",
        "intercomcdn.com",
    },
    "domain": {
        "servd-anthropic-website.b-cdn.net",
        "anthropic.com.cdn.cloudflare.net",
        "anthropic.auth0.com",
        "anthropic-com.ghost.io",
        "browser-intake-us5-datadoghq.com",
        "cdn.usefathom.com",
    },
    "domain_keyword": {"datadog", "sift"},
    "ip_cidr": {"160.79.104.0/21", "2607:6bc0::/32"},
}


def main() -> int:
    data = json.loads(RULE.read_text(encoding="utf-8"))
    if data.get("version") != 2:
        print("version must be 2", file=sys.stderr)
        return 1
    rules = data.get("rules")
    if not isinstance(rules, list) or len(rules) != 1:
        print("rules must contain exactly one rule", file=sys.stderr)
        return 1
    rule = rules[0]
    errors = []
    for key, expected in EXPECTED.items():
        actual = set(rule.get(key, []))
        missing = expected - actual
        if missing:
            errors.append(f"{key} missing: {sorted(missing)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
