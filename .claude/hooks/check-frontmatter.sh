#!/bin/bash
# PostToolUse hook: _posts/*.md 파일의 front matter 검증
# 성공 시 조용히(exit 0), 실패 시 stderr로 경고(exit 2)

INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

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
