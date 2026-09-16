# 이도현 | 기획자의 기술 블로그

경영기획·IT기획 관점의 기술 블로그 — **[dorec9.github.io](https://dorec9.github.io/)**

이 저장소의 핵심은 글이 아니라 시스템이다. 발행의 대부분을 직접 설계한 **AI 자동 발행 하네스**가 수행한다. 규칙·검증 스크립트로 품질을 통제하고, ChatGPT Pro로 인증한 로컬 Codex 예약 작업이 포스트를 한 편씩 발행한다. 사람의 역할은 시스템을 설계하고, 실패를 규칙으로 승격시키는 것이다.

설계 과정은 [하네스 설계 일지](https://dorec9.github.io/categories/harness-engineering/) 카테고리에, 의사결정 기록은 [JOURNEY.md](JOURNEY.md)에 남긴다.

## 자동 발행 파이프라인

```mermaid
flowchart LR
    A["Codex 예약 작업<br>로컬 실행"] --> B["대기열 또는 요일별<br>카테고리 선택"]
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
| 월 | GitHub 레포 분석 → 프로젝트 회고 (project-retrospect) |
| 화 | 직무 인사이트 (planning-insight) |
| 수 | 데이터 분석/통계 (data-statistics) |
| 목 | 트렌드 리서치 (trend-research) |
| 금 | 경영·경제 분석 (business-economy) |

실행 주체는 로컬 Codex 예약 작업이다. 저장소의 [AGENTS.md](AGENTS.md)가 조사·작성·검토·발행 절차를 정의한다. 2026-09-16부터 콘텐츠 발행과 검증을 Codex가 수행한다. 로컬 파일을 사용하는 예약 작업이므로 실행 시 PC와 Codex 앱이 켜져 있어야 한다.

## 하네스 구조

```
.claude/
└── rules/              품질 규칙 4개 (톤 · 금지어 · 출처 · 주제 선정)
AGENTS.md                Codex 자동 발행 절차와 안전장치
_data/
├── topic-history.yml   전체 발행 이력 — 카테고리 간 교차 중복까지 차단
├── seed-keywords.yml   카테고리별 시드 키워드 로테이션
├── publish-backlog.yml 순차 발행 대기열
└── repo-tracker.yml    레포 회고 상태 추적 (커밋 SHA 비교)
_posts/                 발행된 포스트
failures/               실패 레지스트리 — 실패가 규칙이 되는 루프
scripts/validate_post.py 포스트 형식·분량·출처·금지어 검사
```

## 품질 통제 장치

| 장치 | 역할 |
|------|------|
| `rules/blacklist.md` | 과장 수식어 7개, AI 특유 표현 금지. 원칙: 수식어를 빼도 문장이 성립하면 뺀다 |
| `rules/source-policy.md` | 출처를 3단계로 등급화. 출처 불명 자료·AI 출력물 인용 불가 |
| `rules/tone.md` | ~다 체, 1인칭 실무자 시점, 문장 40자 이내 |
| `rules/topic-policy.md` | 발행 이력 대조. 동일 카테고리는 물론 카테고리 간 중복도 금지 |
| `scripts/validate_post.py` | front matter·날짜·분량·출처·금지어를 결정적으로 검사 |
| 한 실행 한 편 | 누락분을 급히 대량 생성하지 않고 각 글을 독립 검증 |
| Jekyll 빌드 | 발행 전에 전체 사이트 빌드를 검증 |
| `failures/registry.md` | 실패 사례 축적, 반복 패턴은 규칙으로 승격 |

## 이력

- **2026-04** — 리눅스에서 초기 구축. tmux + Claude Code REPL cron으로 하루 4포스트 발행
- **2026-07** — 윈도우 이전과 함께 GitHub Actions cron으로 전환. 상시 실행 제거, 하루 1포스트 로테이션
- **2026-09** — 자동 발행 실행 주체를 ChatGPT Pro 기반 Codex 예약 작업으로 전환

## 기술 스택

Jekyll (minimal-mistakes) · GitHub Pages · Codex · Python · Mermaid · Chart.js · KaTeX
