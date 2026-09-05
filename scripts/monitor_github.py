#!/usr/bin/env python3
"""Report the health of every GitHub repository owned by an account."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


API = "https://api.github.com"


def api_get(path: str, token: str | None) -> tuple[object, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-repository-health-monitor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{API}{path}", headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response), dict(response.headers.items())


def all_repositories(owner: str, token: str | None) -> list[dict[str, object]]:
    def pages(path: str) -> list[dict[str, object]]:
        result: list[dict[str, object]] = []
        page = 1
        while True:
            separator = "&" if "?" in path else "?"
            data, _ = api_get(f"{path}{separator}per_page=100&page={page}", token)
            if not isinstance(data, list):
                raise RuntimeError("GitHub returned an unexpected repositories response")
            result.extend(data)
            if len(data) < 100:
                return result
            page += 1

    repositories = pages(f"/users/{quote(owner)}/repos?sort=full_name")
    if token:
        authenticated = pages("/user/repos?affiliation=owner&sort=full_name")
        repositories.extend(
            repository
            for repository in authenticated
            if str(repository.get("owner", {}).get("login", "")).casefold() == owner.casefold()
        )
    return sorted(
        {str(repository["full_name"]): repository for repository in repositories}.values(),
        key=lambda repository: str(repository["full_name"]).casefold(),
    )


def workflow_status(full_name: str, token: str | None) -> tuple[str, str]:
    try:
        data, _ = api_get(
            f"/repos/{full_name}/actions/runs?per_page=1&exclude_pull_requests=true",
            token,
        )
    except HTTPError as error:
        if error.code in (403, 404):
            return "unavailable", "-"
        raise
    runs = data.get("workflow_runs", []) if isinstance(data, dict) else []
    if not runs:
        return "none", "-"
    run = runs[0]
    status = str(run.get("conclusion") or run.get("status") or "unknown")
    return status, str(run.get("html_url") or "-")


def age_in_days(timestamp: str) -> int:
    updated = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return (datetime.now(UTC) - updated).days


def build_report(owner: str, repositories: list[dict[str, object]], token: str | None) -> str:
    lines = [
        f"# GitHub repository health: {owner}",
        "",
        f"Checked at: {datetime.now(UTC).isoformat(timespec='seconds')}",
        "",
        "| Repository | Visibility | Last push | Age | Latest Actions run |",
        "|---|---|---:|---:|---|",
    ]
    for repository in repositories:
        full_name = str(repository["full_name"])
        pushed_at = str(repository.get("pushed_at") or repository["updated_at"])
        status, run_url = workflow_status(full_name, token)
        name = str(repository["name"])
        if name.casefold() == "autobot":
            name = f"**{name} (watched)**"
        repository_url = str(repository["html_url"])
        run = f"[{status}]({run_url})" if run_url != "-" else status
        visibility = "private" if repository.get("private") else "public"
        lines.append(
            f"| [{name}]({repository_url}) | {visibility} | {pushed_at[:10]} "
            f"| {age_in_days(pushed_at)} days | {run} |"
        )
    lines.extend(("", f"Repositories checked: **{len(repositories)}**"))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", default=os.getenv("GITHUB_REPOSITORY_OWNER", "JungyulPark"))
    parser.add_argument("--output", help="also write the Markdown report to this file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    try:
        report = build_report(args.owner, all_repositories(args.owner, token), token)
    except (HTTPError, URLError, RuntimeError) as error:
        print(f"monitor error: {error}", file=sys.stderr)
        return 1
    print(report, end="")
    if args.output:
        with open(args.output, "w", encoding="utf-8") as output:
            output.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
