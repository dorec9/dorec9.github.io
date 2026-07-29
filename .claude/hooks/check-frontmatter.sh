#!/bin/bash
# PostToolUse hook: _posts/*.md 파일의 front matter 검증
# 성공 시 조용히(exit 0), 실패 시 stderr로 경고(exit 2)
# Windows(Git Bash)/리눅스 겸용: 실행 가능한 파이썬을 탐색하고, 없으면 검사를 생략한다

INPUT=$(cat)

# Windows에는 python3가 Store 스텁(실행 불가)인 경우가 있어 실제 실행 여부까지 확인한다
PY=""
for candidate in python3 python py; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "pass" >/dev/null 2>&1; then
    PY="$candidate"
    break
  fi
done
[ -z "$PY" ] && exit 0

FILE=$(printf '%s' "$INPUT" | "$PY" -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Windows 백슬래시 경로를 슬래시로 통일
FILE="${FILE//\\//}"

# _posts/*.md 파일만 검사
[[ "$FILE" != */_posts/*.md ]] && exit 0

# front matter (---) 존재 확인
if [ -f "$FILE" ]; then
  head -1 "$FILE" | grep -q '^---' || {
    echo "front matter 누락: $(basename "$FILE")" >&2
    exit 2
  }
fi

exit 0
