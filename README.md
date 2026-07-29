# 이도현 | 기획자의 기술 블로그

경영기획·IT기획 관점의 기술 블로그 — **[dorec9.github.io](https://dorec9.github.io/)**

이 저장소의 핵심은 글이 아니라 시스템이다. 발행의 대부분을 직접 설계한 **AI 자동 발행 하네스**가 수행한다. 규칙·에이전트·훅으로 품질을 통제하고, GitHub Actions가 평일마다 포스트 1개를 발행한다. 사람의 역할은 시스템을 설계하고, 실패를 규칙으로 승격시키는 것이다.

설계 과정은 [하네스 설계 일지](https://dorec9.github.io/categories/harness-engineering/) 카테고리에 기록한다.

## 자동 발행 파이프라인

```mermaid
flowchart LR
    A["Actions cron<br>평일 09:17 KST"] --> B["요일별<br>카테고리 선택"]
    B --> C["주제 선정<br>발행 이력 중복 검사"]
    C --> D["리서치<br>Tier 1·2 소스만"]
    D --> E["작성<br>톤·금지어 규칙 적용"]
    E --> F["리뷰<br>읽기 전용 검증"]
    F -->|"불합격 시 최대 2회 수정"| E
    F --> G["Jekyll 빌드 검증"]
    G --> H["커밋 · push"]
    H --> I["GitHub Pages 배포"]
```

| 요일 | 발행 내용 |
|------|-----------|
| 월 | GitHub 레포 분석 → 프로젝트 회고 (`/repo-retrospect`) |
| 화 | 직무 인사이트 (planning-insight) |
| 수 | 데이터 분석/통계 (data-statistics) |
| 목 | 트렌드 리서치 (trend-research) |
| 금 | 경영·경제 분석 (business-economy) |

실행 주체는 [claude-code-action](https://github.com/anthropics/claude-code-action) 기반의 [워크플로우](.github/workflows/auto-publish.yml)다. 상시 실행 서버 없이 GitHub Actions 러너에서만 동작한다. 발행 커밋은 GITHUB_TOKEN으로 push되어 워크플로우 재귀 호출이 구조적으로 차단된다.

## 하네스 구조

```
.claude/
├── rules/              품질 규칙 4개 (톤 · 금지어 · 출처 · 주제 선정)
├── skills/             워크플로우 6개 (/auto-publish, /write-post, /review-post, /research, /publish, /repo-retrospect)
├── agents/             writer · reviewer (권한 분리)
├── hooks/              front matter · 빌드 자동 검증 스크립트
└── settings.json       권한 정책 + 훅 연결
_data/
├── topic-history.yml   전체 발행 이력 — 카테고리 간 교차 중복까지 차단
├── seed-keywords.yml   카테고리별 시드 키워드 로테이션
└── repo-tracker.yml    레포 회고 상태 추적 (커밋 SHA 비교)
_posts/                 발행된 포스트
failures/               실패 레지스트리 — 실패가 규칙이 되는 루프
.github/workflows/      auto-publish.yml — 평일 자동 발행
```

## 품질 통제 장치

| 장치 | 역할 |
|------|------|
| `rules/blacklist.md` | 과장 수식어 7개, AI 특유 표현 금지. 원칙: 수식어를 빼도 문장이 성립하면 뺀다 |
| `rules/source-policy.md` | 출처를 3단계로 등급화. 출처 불명 자료·AI 출력물 인용 불가 |
| `rules/tone.md` | ~다 체, 1인칭 실무자 시점, 문장 40자 이내 |
| `rules/topic-policy.md` | 발행 이력 대조. 동일 카테고리는 물론 카테고리 간 중복도 금지 |
| writer / reviewer 분리 | reviewer는 Write·Edit 도구가 없다. 글을 쓴 쪽이 검증하지 않는다 |
| PostToolUse 훅 | 포스트 저장 시마다 front matter 존재를 자동 검사 |
| Stop 훅 | 세션 종료 전 Jekyll 빌드 검증. 깨진 상태로 끝내지 못한다 |
| `failures/registry.md` | 실패 사례 축적, 반복 패턴은 규칙으로 승격 |

## 이력

- **2026-04** — 리눅스에서 초기 구축. tmux + Claude Code REPL cron으로 하루 4포스트 발행
- **2026-07** — 윈도우 이전과 함께 GitHub Actions cron으로 전환. 상시 실행 제거, 하루 1포스트 로테이션

## 기술 스택

Jekyll (minimal-mistakes) · GitHub Pages · GitHub Actions · Claude Code (claude-code-action) · Mermaid · Chart.js · KaTeX
