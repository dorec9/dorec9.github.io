#!/bin/bash
# Stop hook: 세션 종료 시 Jekyll 빌드 검증
# Ruby/bundler/의존성이 없는 환경에서는 조용히 생략한다 — 최종 빌드는 GitHub Pages가 수행

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
command -v bundle >/dev/null 2>&1 || exit 0
bundle check >/dev/null 2>&1 || exit 0

bundle exec jekyll build > /dev/null 2>&1 || {
  echo 'Jekyll 빌드 실패 — bundle exec jekyll build로 확인하세요' >&2
  exit 2
}

exit 0
