#!/bin/bash
# Stop hook: 세션 종료 시 Jekyll 빌드 검증
# Ruby/bundler/의존성이 없는 환경에서는 조용히 생략한다 — 최종 빌드는 GitHub Pages가 수행

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
command -v bundle >/dev/null 2>&1 || exit 0
bundle check >/dev/null 2>&1 || exit 0

BUILD_LOG=$(bundle exec jekyll build 2>&1)
if [ $? -eq 0 ]; then
  exit 0
fi

# 알려진 환경 비호환 오류(failures/registry.md 2026-07-31 기록)는 통과시킨다.
# Gemfile.lock이 github-pages gem으로 jekyll 3.9.0/liquid 4.0.3에 고정되어 있는데
# liquid 4.0.3이 Ruby 3.2+에서 제거된 Object#tainted?를 호출해 실패한다.
# 콘텐츠와 무관하며 실제 배포는 GitHub Pages 자체 빌드 인프라가 수행한다.
if echo "$BUILD_LOG" | grep -q "undefined method .tainted?. for nil"; then
  echo "Jekyll 빌드: 알려진 Ruby/liquid 비호환 오류(failures/registry.md 참조) — 통과 처리" >&2
  exit 0
fi

echo 'Jekyll 빌드 실패 — bundle exec jekyll build로 확인하세요' >&2
exit 2
