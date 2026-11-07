"""Archive GitHub's 14-day aggregate traffic counters; never store tokens or visitor IDs."""

from __future__ import annotations

import json
import os
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone

OUT = pathlib.Path("traffic/history.json")


def request_metric(repo: str, token: str, metric: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/traffic/{metric}"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "research-agent-harness-guide-traffic-archive",
        },
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)


def merge_daily(existing: dict, views: dict, clones: dict) -> dict:
    history = dict(existing)
    history.setdefault("schema_version", 1)
    daily = dict(history.get("daily", {}))
    for metric, data in (("views", views), ("clones", clones)):
        for item in data.get(metric, []):
            day = item["timestamp"][:10]
            if len(day) != 10 or not all(c.isdigit() or c == "-" for c in day):
                raise ValueError("Invalid traffic date")
            row = dict(daily.get(day, {}))
            row[metric] = {
                "count": int(item["count"]),
                "uniques": int(item["uniques"]),
            }
            daily[day] = row
    history["daily"] = dict(sorted(daily.items()))
    return history


def main() -> None:
    token = os.environ.get("TRAFFIC_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        raise SystemExit("Missing TRAFFIC_TOKEN or GITHUB_REPOSITORY")
    if repo.count("/") != 1 or any(x not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._/" for x in repo):
        raise SystemExit("Invalid repository identifier")
    try:
        views = request_metric(repo, token, "views")
        clones = request_metric(repo, token, "clones")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"GitHub traffic API returned HTTP {exc.code}; check token permissions") from None
    existing = json.loads(OUT.read_text()) if OUT.exists() else {}
    merged = merge_daily(existing, views, clones)
    merged["last_collected_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n")
    print(f"Archived aggregate daily traffic for {len(merged['daily'])} dates.")


if __name__ == "__main__":
    main()
