# Blog Automation Harness

## Project
- 취업용 기술 블로그 (경영기획/IT기획 타겟)
- GitHub Pages + Jekyll (minimal-mistakes, air 스킨)
- 하네스 엔지니어링으로 AI 에이전트 블로그 자동화

## Rules
- IMPORTANT: 한국어 작성, 실무자 시점, ~다 체
- IMPORTANT: 과장 표현 금지 — .claude/rules/blacklist.md 참조
- YOU MUST: 모든 주장에 데이터/소스 근거 포함 — .claude/rules/source-policy.md 참조
- YOU MUST: 포스트 작성 시 front matter 필수 (title, date, categories, tags, excerpt)
- 커밋 메시지 한국어

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

## Skills
- `/write-post [주제]` — 블로그 글 생성
- `/review-post [파일]` — 글 품질 검증
- `/publish [메시지]` — Git commit + push
- `/research [키워드]` — 트렌드/데이터 수집

## Failure Tracking
- 실패 패턴은 failures/registry.md에 기록
- 반복되는 실패는 .claude/rules/에 규칙으로 승격
