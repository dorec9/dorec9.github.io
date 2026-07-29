# Blog Automation Harness

## Project
- 취업용 기술 블로그 (경영기획/IT기획 타겟)
- GitHub Pages + Jekyll (minimal-mistakes, air 스킨)
- 하네스 엔지니어링으로 AI 에이전트 블로그 자동화

## Environment
- 작업 환경: Windows 11 + Git Bash (2026-07-29 리눅스에서 이전)
- 훅은 `bash .claude/hooks/*.sh`로 실행 — Git Bash 필수
- `python3`는 Windows Store 스텁이라 실행 불가 — 스크립트는 `python` 폴백 사용
- 로컬 Ruby/Jekyll 미설치 — 빌드 검증 훅은 bundler 있을 때만 동작, 최종 빌드는 GitHub Pages가 수행

## Rules
- IMPORTANT: 한국어 작성, 실무자 시점, ~다 체
- IMPORTANT: 과장 표현 금지 — .claude/rules/blacklist.md 참조
- YOU MUST: 모든 주장에 데이터/소스 근거 포함 — .claude/rules/source-policy.md 참조
- YOU MUST: 포스트 작성 시 front matter 필수 (title, date, categories, tags, excerpt)
- 커밋 메시지 한국어
- YOU MUST NOT: 커밋 메시지에 Co-Authored-By 절대 넣지 않는다

## Categories
| 카테고리 | 슬러그 |
|----------|--------|
| 프로젝트 회고 | project-retrospect |
| 직무 인사이트 | planning-insight |
| 데이터 분석/통계 | data-statistics |
| 트렌드 리서치 | trend-research |
| 경영·경제 분석 | business-economy |
| 하네스 설계 일지 | harness-engineering |

## Build
```bash
bundle exec jekyll build
bundle exec jekyll serve   # http://localhost:4000
```
- 로컬에 Ruby/bundler가 없으면 생략한다 — push 후 GitHub Pages가 원격 빌드

## Skills
- `/write-post [주제]` — 블로그 글 생성
- `/review-post [파일]` — 글 품질 검증
- `/publish [메시지]` — Git commit + push
- `/research [키워드]` — 트렌드/데이터 수집
- `/auto-publish [카테고리slug]` — 자동 발행 파이프라인 (주제 선정→리서치→작성→근거 캡처→리뷰→발행)
- `/repo-retrospect` — GitHub public 레포 분석 후 프로젝트 회고 포스트 자동 발행

## Auto-Publish Schedule
- GitHub Actions cron으로 자동 발행 (`.github/workflows/auto-publish.yml`) — 로컬 상시 실행 불필요
- 평일 09:17 KST 하루 1포스트 로테이션: 월=repo-retrospect, 화=planning-insight, 수=data-statistics, 목=trend-research, 금=business-economy
- 수동 실행: Actions 탭에서 workflow_dispatch (task 입력으로 특정 카테고리 지정 가능)
- 인증: repo secret `CLAUDE_CODE_OAUTH_TOKEN` (`claude setup-token`으로 발급)
- 구 방식(리눅스 tmux + REPL cron, 하루 4개)은 2026-07 윈도우 이전과 함께 폐기
- 수동: harness-engineering (/write-post 사용)

## A/B Experiment
- exp1 (2026-07-30 시작): 홈/목록의 글 요약(excerpt) 표시(A) vs 숨김(B)
- 배정: localStorage `ab_exp1_variant` 50/50 → `html[data-ab-exp1]` 속성 (head/custom.html)
- 측정: GA4 `G-Q0E5NGW6L6` — user property `ab_exp1`, 이벤트 `list_post_click` (custom.js)
- 지표: 목록→글 클릭률
- YOU MUST NOT: 실험 종료 전 목록 UI·excerpt·실험 코드를 변경하지 않는다

## Data Files
- `_data/topic-history.yml` — 전체 카테고리 주제 발행 이력 (중복 방지용)
- `_data/repo-tracker.yml` — GitHub 레포 분석 상태 추적
- `_data/seed-keywords.yml` — 카테고리별 시드 키워드 목록

## Failure Tracking
- 실패 패턴은 failures/registry.md에 기록
- 반복되는 실패는 .claude/rules/에 규칙으로 승격
