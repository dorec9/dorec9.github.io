#!/usr/bin/env python3
"""자동 발행 포스트의 최소 품질 계약을 검사한다."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED = ("title", "date", "categories", "tags", "excerpt")
VALID_CATEGORIES = {
    "project-retrospect",
    "planning-insight",
    "data-statistics",
    "trend-research",
    "business-economy",
    "harness-engineering",
}
BLOCKED = (
    "혁신적인",
    "획기적인",
    "놀라운",
    "강력한",
    "완벽한",
    "최적의",
    "궁극적인",
    "살펴보겠습니다",
    "해 보도록 하겠습니다",
    "마무리하며",
    "지금까지",
    "세계로 떠나볼까요",
    "대기열 기준일",
    "자료는 202",
    "누락분을",
    "밀린 글",
    "자동화 장애",
    "복구 작업",
)


def fail(messages: list[str]) -> int:
    for message in messages:
        print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        return fail(["사용법: python scripts/validate_post.py _posts/YYYY-MM-DD-slug.md"])

    path = Path(sys.argv[1])
    if not path.is_file():
        return fail([f"파일을 찾을 수 없음: {path}"])

    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", text, re.S)
    if not match:
        return fail(["YAML front matter 구분자가 없거나 형식이 잘못됨"])

    header, body = match.groups()
    fields: dict[str, str] = {}
    for line in header.splitlines():
        field = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if field:
            fields[field.group(1)] = field.group(2).strip().strip('"\'')

    errors: list[str] = []
    for name in REQUIRED:
        if not fields.get(name):
            errors.append(f"front matter 필수 필드 누락: {name}")

    filename_date = re.match(r"^(\d{4}-\d{2}-\d{2})-", path.name)
    if not filename_date:
        errors.append("파일명이 YYYY-MM-DD-slug.md 형식이 아님")
    elif fields.get("date") != filename_date.group(1):
        errors.append("파일명 날짜와 front matter date가 다름")

    if fields.get("categories") not in VALID_CATEGORIES:
        errors.append(f"허용되지 않은 categories: {fields.get('categories', '')}")

    if len(fields.get("excerpt", "")) > 100:
        errors.append("excerpt가 100자를 초과함")

    for phrase in BLOCKED:
        if phrase in body:
            errors.append(f"금지 표현 포함: {phrase}")

    links = re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", body)
    if len(links) < 3:
        errors.append(f"본문 외부 출처가 3개 미만: {len(links)}개")

    visible_text = re.sub(r"```.*?```", "", body, flags=re.S)
    visible_text = re.sub(r"<[^>]+>", "", visible_text)
    if len(visible_text.strip()) < 1500:
        errors.append(f"본문 분량이 1,500자 미만: {len(visible_text.strip())}자")
    if len(visible_text.strip()) > 6000:
        errors.append(f"본문 분량이 6,000자를 초과함: {len(visible_text.strip())}자")

    if re.search(r"\[(여기|링크)\]\(", body):
        errors.append("서술적이지 않은 링크 텍스트 사용")

    if errors:
        return fail(errors)

    print(f"OK: {path} ({len(visible_text.strip())}자, 외부 출처 {len(links)}개)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
