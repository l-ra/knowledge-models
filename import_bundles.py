#!/usr/bin/env python3
"""Import release bundle JSON files into a running knowledge-core.

Usage:
  python3 import_bundles.py path/to/a.bundle.json [path/to/b.bundle.json ...]

Auth (dev KC assumptions, KC_AUTH_MODE=bootstrap by default):
  1. KC_TOKEN or KC_ADMIN_PASSWORD — Bearer + X-Admin-Password
  2. KC_BOOTSTRAP_PASSWORD_FILE, else sibling knowledge-core/.tmp/admin.password
  3. else X-Subject / X-Roles (KC_AUTH_MODE=dev)

Env:
  KC_BASE_URL   default http://localhost:8080
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODELS_ROOT = Path(__file__).resolve().parent


def resolve_bootstrap_password() -> str | None:
    explicit = (
        os.environ.get("KC_TOKEN")
        or os.environ.get("KC_ADMIN_PASSWORD")
        or ""
    ).strip()
    if explicit:
        return explicit

    candidates: list[Path] = []
    env_file = (os.environ.get("KC_BOOTSTRAP_PASSWORD_FILE") or "").strip()
    if env_file:
        candidates.append(Path(env_file))
    # scripts/dev.sh default when knowledge-models sits next to knowledge-core
    candidates.append(MODELS_ROOT.parent / "knowledge-core" / ".tmp" / "admin.password")
    candidates.append(Path("/data/admin.password"))

    for path in candidates:
        try:
            if path.is_file() and path.stat().st_size > 0:
                return path.read_text().strip()
        except OSError:
            continue
    return None


def auth_headers() -> dict[str, str]:
    h = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    token = resolve_bootstrap_password()
    if token:
        h["Authorization"] = f"Bearer {token}"
        h["X-Admin-Password"] = token
    else:
        h["X-Subject"] = os.environ.get("KC_SUBJECT", "admin")
        h["X-Roles"] = os.environ.get("KC_ROLES", "admin")
    return h


def unwrap(body: dict) -> dict:
    if isinstance(body.get("data"), dict):
        return body["data"]
    return body


def post_bundle(base: str, headers: dict[str, str], path: Path) -> tuple[int, dict]:
    raw = path.read_bytes()
    url = base.rstrip("/") + "/v1/releases/import"
    req = urllib.request.Request(url, data=raw, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            body_raw = resp.read()
            body = json.loads(body_raw) if body_raw else {}
            return resp.status, body
    except urllib.error.HTTPError as e:
        body_raw = e.read()
        try:
            body = json.loads(body_raw) if body_raw else {}
        except json.JSONDecodeError:
            body = {"error": body_raw.decode("utf-8", "replace")}
        return e.code, body


def bundle_label(path: Path) -> str:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return path.name
    manifest = data.get("manifest") or {}
    code = manifest.get("package") or manifest.get("packageCode") or "?"
    version = manifest.get("version") or "?"
    return f"{code}@{version}"


def resolve_path(arg: str) -> Path:
    p = Path(arg)
    if p.is_file():
        return p.resolve()
    alt = MODELS_ROOT / arg
    if alt.is_file():
        return alt.resolve()
    raise SystemExit(f"bundle not found: {arg}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Import release bundles into knowledge-core (POST /v1/releases/import).",
    )
    ap.add_argument(
        "bundles",
        nargs="+",
        metavar="BUNDLE",
        help="Paths to *.bundle.json (cwd or repo-relative)",
    )
    args = ap.parse_args(argv)

    base = os.environ.get("KC_BASE_URL", "http://localhost:8080")
    headers = auth_headers()

    try:
        health = urllib.request.Request(base.rstrip("/") + "/healthz", method="GET")
        with urllib.request.urlopen(health) as resp:
            if resp.status != 200:
                print(f"warning: {base}/healthz -> {resp.status}", file=sys.stderr)
    except urllib.error.URLError as e:
        raise SystemExit(f"cannot reach {base}: {e}") from e

    paths = [resolve_path(a) for a in args.bundles]
    for path in paths:
        label = bundle_label(path)
        print(f"--- importing {label} ({path}) ---")
        status, body = post_bundle(base, headers, path)
        if status not in (200, 201):
            raise SystemExit(f"import {label}: HTTP {status}: {body}")
        data = unwrap(body) if isinstance(body, dict) else {}
        code = data.get("package") or data.get("packageCode") or "?"
        version = data.get("version") or "?"
        replay = " (replay)" if status == 200 else ""
        print(f"ok {code}@{version}{replay}")

    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
