#!/usr/bin/env python3
"""클라우드 발행의 날짜·변경 파일·단일 포스트 계약을 확인한다."""

from __future__ import annotations

import re
import subprocess
import sys
import os
import time
import urllib.error
import urllib.request
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def git(*args: str) -> list[str]:
    return subprocess.check_output(["git", *args], text=True).splitlines()


def today() -> str:
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")


def post_paths(day: str) -> list[Path]:
    return list(Path("_posts").glob(f"{day}-*.md"))


def preflight() -> None:
    day = today()
    weekday = datetime.now(ZoneInfo("Asia/Seoul")).weekday()
    publish = weekday < 5 and not post_paths(day)
    print(f"publish={'true' if publish else 'false'}")
    print(f"date={day}")


def verify() -> None:
    day = today()
    if not post_paths(day) and datetime.now(ZoneInfo("Asia/Seoul")).weekday() == 0:
        changed = git("status", "--porcelain")
        if changed:
            raise ValueError("월요일 무발행 시 파일 변경이 없어야 합니다")
        print("post=")
        return
    if len(post_paths(day)) != 1:
        raise ValueError(f"{day} 날짜의 포스트가 정확히 한 편이어야 합니다")
    new_posts = git("ls-files", "--others", "--exclude-standard", "--", "_posts")
    if len(new_posts) != 1 or Path(new_posts[0]) != post_paths(day)[0]:
        raise ValueError("오늘 날짜의 새 포스트 한 편만 생성해야 합니다")
    modified = set(git("diff", "--name-only"))
    allowed = {"_data/topic-history.yml", "_data/repo-tracker.yml"}
    if not modified.issubset(allowed) or "_data/topic-history.yml" not in modified:
        raise ValueError(f"허용되지 않거나 누락된 변경: {sorted(modified)}")
    untracked = set(git("ls-files", "--others", "--exclude-standard"))
    if untracked != set(new_posts):
        raise ValueError(f"포스트 외 새 파일이 있습니다: {sorted(untracked - set(new_posts))}")
    path = new_posts[0]
    Path("/tmp/dorec9-cloud-post-path").write_text(path, encoding="utf-8")
    print(f"post={path}")


def title(path: str) -> None:
    body = Path(path).read_text(encoding="utf-8")
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', body, re.MULTILINE)
    if not match:
        raise ValueError("포스트 title이 없습니다")
    print(match.group(1).strip('"\''))


def pages(path: str) -> None:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise ValueError("GH_TOKEN이 없습니다")
    repo = os.environ["GITHUB_REPOSITORY"]
    api = f"https://api.github.com/repos/{repo}/pages/builds"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "dorec9-cloud-publisher",
    }
    with urllib.request.urlopen(urllib.request.Request(api, headers=headers, method="POST")):
        pass
    head = git("rev-parse", "HEAD")[0]
    for _ in range(60):
        with urllib.request.urlopen(urllib.request.Request(api + "/latest", headers=headers)) as response:
            build = json.load(response)
        if build.get("commit") == head and build.get("status") == "built":
            break
        if build.get("commit") == head and build.get("status") in {"errored", "failed"}:
            raise ValueError(f"Pages 빌드 실패: {build.get('error')}")
        time.sleep(10)
    else:
        raise ValueError("새 커밋의 Pages 빌드가 10분 안에 완료되지 않았습니다")

    name = Path(path).stem
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})-(.+)", name)
    if not match:
        raise ValueError("포스트 파일명 형식이 올바르지 않습니다")
    year, month, day, slug = match.groups()
    body = Path(path).read_text(encoding="utf-8")
    category = re.search(r"^categories:\s*([a-z-]+)\s*$", body, re.MULTILINE)
    if not category:
        raise ValueError("categories를 찾을 수 없습니다")
    url = f"https://dorec9.github.io/{category.group(1)}/{year}/{month}/{day}/{slug}.html"
    for _ in range(30):
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode("utf-8")
            if title_text(body) in html:
                print(f"Pages 게시 확인: {url}")
                return
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
        time.sleep(10)
    raise ValueError(f"Pages 빌드 후에도 글이 보이지 않습니다: {url}")


def title_text(body: str) -> str:
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', body, re.MULTILINE)
    if not match:
        raise ValueError("포스트 title이 없습니다")
    return match.group(1).strip('"\'')


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "preflight":
            preflight()
        elif len(sys.argv) == 2 and sys.argv[1] == "verify":
            verify()
        elif len(sys.argv) == 3 and sys.argv[1] == "title":
            title(sys.argv[2])
        elif len(sys.argv) == 3 and sys.argv[1] == "pages":
            pages(sys.argv[2])
        else:
            raise ValueError("preflight | verify | title <포스트 경로>")
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
