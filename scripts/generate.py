#!/usr/bin/env python3
"""Generate sing-box compatible rule-set artifacts from source/claude-full.yaml."""
from __future__ import annotations

import json
import pathlib
import sys

try:
    import yaml
except ImportError:
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "claude-full.yaml"
OUT_JSON = ROOT / "rule-set" / "claude-full.json"
OUT_TXT = ROOT / "rule-set" / "claude-full.list"


def minimal_yaml_load(text: str) -> dict:
    """Tiny YAML subset parser for this repository if PyYAML is unavailable."""
    data: dict[str, object] = {}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not raw.startswith(" ") and line.endswith(":"):
            current = line[:-1].strip()
            data[current] = []
        elif not raw.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
            current = None
        elif current and line.strip().startswith("- "):
            data[current].append(line.strip()[2:].strip())
    return data


def load_source() -> dict:
    text = SOURCE.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return minimal_yaml_load(text)


def dedupe(seq: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in seq:
        item = str(item).strip()
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def main() -> int:
    src = load_source()
    rule = {}
    for key in ("domain_suffix", "domain", "domain_keyword", "ip_cidr"):
        values = dedupe(src.get(key, []) or [])
        if values:
            rule[key] = values

    payload = {"version": 2, "rules": [rule]}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = []
    for value in rule.get("domain_suffix", []):
        lines.append(f"DOMAIN-SUFFIX,{value}")
    for value in rule.get("domain", []):
        lines.append(f"DOMAIN,{value}")
    for value in rule.get("domain_keyword", []):
        lines.append(f"DOMAIN-KEYWORD,{value}")
    for value in rule.get("ip_cidr", []):
        prefix = "IP-CIDR6" if ":" in value else "IP-CIDR"
        lines.append(f"{prefix},{value},no-resolve")
    for value in dedupe(src.get("ip_asn", []) or []):
        lines.append(f"IP-ASN,{value},no-resolve")
    OUT_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_TXT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
