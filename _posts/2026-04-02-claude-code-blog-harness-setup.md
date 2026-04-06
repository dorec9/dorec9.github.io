---
title: "Claude Code 하네스로 블로그 자동화 시스템 구축한 과정"
date: 2026-04-02
categories: harness-engineering
tags: [Claude-Code, 하네스엔지니어링, 블로그자동화, Skills, Hooks, Cron, 자동발행]
excerpt: "규칙 4개, 스킬 7개, 에이전트 2개, 훅 2개, cron 자동 발행까지 — 블로그 품질 관리 파이프라인을 만들고 확장한 과정을 정리했다."
---

## 왜 이 하네스를 만들었나

취업용 기술 블로그를 운영하기로 했다. 경영기획/IT기획 직무 타겟이라 글의 톤과 근거가 중요하다. 그런데 AI에게 "글 써줘"만 하면 과장 표현이 나온다. 출처 없는 주장도 섞인다. 그래서 규칙 기반으로 품질을 통제하는 하네스를 설계했다.

하네스 엔지니어링은 AI 에이전트의 환경·규칙·도구를 설정해서 출력 품질을 높이는 방법론이다([NxCode 가이드](https://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026)). Claude Code는 CLAUDE.md, Skills, Hooks, Agents 4가지 메커니즘을 제공한다([공식 문서](https://code.claude.com/docs/en/how-claude-code-works)).

---

## 전체 구조

설계한 하네스의 초기 구조(2026-04-02 기준)는 이렇다. 이후 확장 내용은 하단 업데이트 섹션을 참고한다.

```
.claude/
├── settings.json          # 권한 + 훅
├── rules/                 # 품질 규칙 3개
│   ├── tone.md            # 톤앤매너
│   ├── blacklist.md       # 금지 표현
│   └── source-policy.md   # 소스 신뢰도
├── skills/                # 슬래시 커맨드 4개
│   ├── write-post/
│   ├── review-post/
│   ├── research/
│   └── publish/
├── agents/                # 전문 에이전트 2개
│   ├── writer.md
│   └── reviewer.md
└── hooks/
    └── check-frontmatter.sh  # 자동 검증 스크립트
```

구성 요소는 총 11개 파일이다. 각각의 역할을 설명한다.

---

## 1. 규칙 파일 — 품질의 기준선

`.claude/rules/` 디렉토리에 3개 규칙 파일을 만들었다. Claude Code는 이 디렉토리의 마크다운을 자동으로 읽는다. 모든 작업에 적용된다.

### tone.md — 문체 통제

핵심 규칙 4가지:

| 항목 | 규칙 |
|------|------|
| 문체 | ~다 체 (경어체 금지) |
| 시점 | 1인칭 실무자 ("내가 해봤더니") |
| 문장 길이 | 40자 이내 권장 |
| 구성 | 서두(왜) → 본문(과정) → 결론(배운 점) |

### blacklist.md — 금지 표현

AI가 자주 쓰는 표현을 명시적으로 차단했다. 2가지 유형으로 나눈다.

**과장 수식어 7개** (사용 불가): "혁신적인", "획기적인", "놀라운", "강력한", "완벽한", "최적의", "궁극적인"

**빈 수식어** (수치로 대체 필수): "다양한" → 구체적 개수, "효과적인" → 지표와 수치, "빠르게" → 소요 시간 명시

원칙은 하나다. 수식어를 빼도 문장이 성립하면 빼라.

### source-policy.md — 소스 신뢰도 3단계

| Tier | 설명 | 정책 |
|------|------|------|
| 1 | 공식 문서, 학술 논문, 정부 통계 | 인용 가능 |
| 2 | 기술 블로그, 언론 보도, GitHub 레포 | 출처 명시 필수 |
| 3 | 출처 불명, 커뮤니티 루머, AI 출력물 | 사용 불가 |

2년 이상 된 자료는 "(YYYY년 기준)"을 붙이도록 했다.

---

## 2. 스킬 — 워크플로우 자동화

스킬은 Claude Code의 슬래시 커맨드다([Skills 문서](https://code.claude.com/docs/en/skills)). `.claude/skills/`에 SKILL.md 파일로 정의한다. 4개를 만들었다.

### /research — 데이터 수집

```
입력: /research [키워드]
동작: WebSearch 3회 이상 → Tier 1-2만 채택 → 구조화된 노트 출력
컨텍스트: fork (별도 컨텍스트에서 실행)
```

fork 컨텍스트로 설정한 이유가 있다. 리서치는 검색 결과가 많아서 메인 대화의 컨텍스트를 오염시킨다. 별도 컨텍스트에서 실행하면 메인 대화 창에는 정리된 결과만 남는다.

### /write-post — 글 작성

```
입력: /write-post [주제]
동작: 리서치 → 아웃라인(3-7섹션) → 본문(1,500-3,000자) → front matter → 저장
출력: _posts/YYYY-MM-DD-slug.md
```

allowed-tools에 WebSearch와 WebFetch를 포함해서 작성 중 실시간 근거 수집이 가능하다.

### /review-post — 품질 검증

```
입력: /review-post [파일경로]
검증: front matter 완성도, 블랙리스트, 소스 정책, 톤, 분량
출력: 합격/불합격 + 수정 제안
```

이 스킬의 핵심은 **읽기 전용**이다. allowed-tools에 Read, Grep, Glob만 넣었다. Write와 Edit를 빼서 검증 도중 파일을 임의로 수정하는 것을 원천 차단했다.

### /publish — 발행

```
입력: /publish [커밋메시지]
동작: git status → Jekyll 빌드 검증 → git add → git commit
안전장치: 빌드 실패 시 중단, push 전 사용자 확인
```

`disable-model-invocation: true`로 설정했다. 발행은 단순 셸 명령 실행이라 LLM 호출이 필요 없다. 불필요한 토큰 소모를 방지한다.

---

## 3. 에이전트 — 역할 분리

에이전트는 `.claude/agents/` 디렉토리에 정의한다. 스킬이 워크플로우 단위라면, 에이전트는 역할 단위다. 2개를 만들었다.

| 에이전트 | 역할 | 모델 | 도구 제한 |
|----------|------|------|-----------|
| writer | 포스트 작성 | Sonnet | Read, Write, Edit, WebSearch 등 7개 |
| reviewer | 품질 검증 | Sonnet | Read, Grep, Glob 3개만 (Write/Edit 차단) |

writer와 reviewer를 분리한 이유는 검증의 독립성 때문이다. 글을 쓴 에이전트가 직접 검증하면 자기 산출물에 관대해진다. reviewer는 파일 수정 권한 자체가 없으니 순수하게 검증만 한다.

---

## 4. 훅 — 자동 안전장치

settings.json에 2개 훅을 설정했다.

### PostToolUse 훅 — front matter 검증

```json
{
  "matcher": "Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/check-frontmatter.sh\""
  }]
}
```

Edit이나 Write 도구가 실행될 때마다 자동으로 `check-frontmatter.sh`를 실행한다. `_posts/*.md` 파일에 YAML front matter(`---`)가 없으면 exit 2로 경고한다. Jekyll은 front matter가 없으면 마크다운을 처리하지 않는다. 그래서 이 검증이 필요하다.

### Stop 훅 — 빌드 검증

```json
{
  "hooks": [{
    "type": "command",
    "command": "cd \"$CLAUDE_PROJECT_DIR\" && bundle exec jekyll build > /dev/null 2>&1 || { echo 'Jekyll 빌드 실패' >&2; exit 2; }"
  }]
}
```

Claude Code 세션이 종료될 때 Jekyll 빌드를 실행한다. 빌드가 실패하면 exit 2를 반환해서 세션 종료를 차단한다. 깨진 상태로 작업을 끝내는 것을 방지하는 마지막 안전망이다.

---

## 5. 권한 설정 — 허용과 차단

settings.json의 permissions 섹션으로 Claude Code가 실행할 수 있는 명령을 제한했다.

**허용 목록 (8개):**
- `bundle exec *` — Jekyll 빌드/서브
- `git status`, `git add *`, `git commit *`, `git diff *`, `git log *` — Git 기본 작업
- `WebSearch` — 웹 검색

**차단 목록 (3개):**
- `rm -rf *` — 대량 삭제
- `git push --force *` — 강제 푸시
- `git reset --hard *` — 하드 리셋

차단 목록은 복구 불가능한 작업 위주로 구성했다. 전체 파일 삭제, 커밋 히스토리 덮어쓰기를 원천 차단한다.

---

## 6. 실패 추적 — 점진적 개선 루프

`failures/registry.md`에 실패 패턴을 기록하는 구조를 만들었다. 형식은 이렇다:

```
### YYYY-MM-DD: [실패 유형]
- 상황:
- 기대:
- 실제:
- 원인:
- 조치: (규칙 추가/수정 여부)
```

톤 위반, 블랙리스트 미검출, 소스 정책 위반, 빌드 실패 카테고리로 분류한다. 반복되는 패턴이 발견되면 `.claude/rules/`에 새 규칙으로 승격시킨다. 실패가 규칙이 되고, 규칙이 품질이 되는 루프다.

---

## 워크플로우 요약

전체 파이프라인은 4단계다.

```
/research [키워드]     리서치 (Tier 1-2 소스만)
        ↓
/write-post [주제]     작성 (규칙 3개 적용)
        ↓
/review-post [파일]    검증 (읽기 전용, 5개 항목)
        ↓
/publish               발행 (빌드 검증 → 커밋)
```

각 단계마다 품질 게이트가 있다. 리서치에서 Tier 3 소스를 걸러내고, 작성에서 블랙리스트를 적용하고, 검증에서 누락을 잡고, 발행에서 빌드를 확인한다.

---

## 배운 점

하네스를 만들면서 느낀 3가지:

1. **규칙은 구체적일수록 작동한다.** "좋은 글을 써라"는 규칙은 무의미하다. "혁신적인 사용 금지"처럼 단어 단위로 지정해야 AI가 따른다.

2. **권한 분리가 품질을 만든다.** writer에게 검증을, reviewer에게 수정 권한을 주면 역할이 무너진다. 도구 접근 제한이 가장 확실한 역할 분리다.

3. **훅은 사람의 실수를 막는다.** front matter를 빠뜨리거나 빌드가 깨진 채로 커밋하는 건 AI가 아니라 사람의 실수다. 자동 검증이 이를 잡는다.

다음 단계는 실패 레지스트리에 사례를 축적하면서 규칙을 고도화하는 것이다. 하네스는 한 번 만들고 끝이 아니라, 실패에서 배우는 시스템이다.

---

## 2026-04-06 업데이트 — 자동 발행 시스템으로 확장

초기 구축 이후 4일간 하네스를 운영하면서 구조가 확장되었다. 규칙 3개 → 4개, 스킬 4개 → 7개, 데이터 파일 0개 → 3개로 늘었다. 변경 내역을 정리한다.

### 현재 파일 구조

```
.claude/
├── settings.json
├── rules/                 # 4개 (+1)
│   ├── tone.md
│   ├── blacklist.md
│   ├── source-policy.md
│   └── topic-policy.md    ← 신규
├── skills/                # 7개 (+3)
│   ├── write-post/
│   ├── review-post/
│   ├── research/
│   ├── publish/
│   ├── auto-publish/      ← 신규
│   ├── repo-retrospect/   ← 신규
│   └── setup-schedules/   ← 신규
├── agents/
│   ├── writer.md
│   └── reviewer.md
└── hooks/
    └── check-frontmatter.sh

_data/                     # 데이터 인프라 (+3)
├── topic-history.yml      ← 신규
├── seed-keywords.yml      ← 신규
└── repo-tracker.yml       ← 신규
```

### 규칙 추가: topic-policy.md

글이 쌓이면서 주제 중복 문제가 생겼다. 같은 키워드를 다른 카테고리에서 반복하거나, 비슷한 제목의 글이 나왔다. topic-policy.md를 추가해 3가지를 강제했다.

1. 작성 전 `_data/topic-history.yml`에서 기존 발행 이력을 확인한다
2. 동일 카테고리 내 중복 금지, 카테고리 간 교차 중복도 방지한다
3. `_data/seed-keywords.yml`에서 최근 미사용 키워드를 우선 선택한다

### 스킬 3개 추가

**`/auto-publish [카테고리]` — 6단계 일괄 파이프라인**

초기에는 /research → /write-post → /review-post → /publish를 수동으로 순서대로 실행했다. auto-publish는 이 4단계에 주제 선정과 히스토리 갱신을 추가해서 6단계를 자동으로 실행한다.

```
1. 주제 선정 (topic-history + seed-keywords 참조)
2. 리서치 (Tier 1-2 소스 최소 3개)
3. 작성 (write-post 호출)
4. 리뷰 (review-post 호출, 불합격 시 최대 2회 재시도)
5. 히스토리 갱신 (topic-history.yml 업데이트)
6. 발행 (빌드 검증 → 커밋 → 푸시)
```

리뷰에서 3회 연속 불합격하면 `failures/registry.md`에 기록하고 중단한다.

**`/repo-retrospect` — GitHub 레포 분석 회고**

GitHub API로 dorec9의 public 레포를 조회하고, `_data/repo-tracker.yml`과 비교해서 아직 회고하지 않은 레포나 변경이 발생한 레포를 찾는다. README, 커밋 로그, 디렉토리 구조를 분석해서 프로젝트 회고 포스트를 자동 생성한다. 기존 회고가 있는 레포에 변경이 생기면 업데이트 섹션을 추가한다.

**`/setup-schedules` — cron 자동 발행 등록**

5개 카테고리의 cron 스케줄을 일괄 등록한다.

| 카테고리 | 실행 시각 | 주기 |
|---------|----------|------|
| planning-insight | 08:23 | 평일 |
| data-statistics | 09:47 | 평일 |
| trend-research | 11:13 | 평일 |
| business-economy | 12:53 | 평일 |
| project-retrospect | 14:37 | 월요일 |

각 job 사이에 1시간 이상 간격을 둬서 git 충돌을 방지한다. 정각(:00, :30)은 의도적으로 피했다. Claude Code REPL이 tmux에서 상시 실행 중이어야 cron이 동작한다.

### 데이터 인프라 3개

| 파일 | 용도 |
|------|------|
| `topic-history.yml` | 전체 카테고리 발행 이력. 주제 중복 방지의 핵심 데이터 |
| `seed-keywords.yml` | auto-publish 대상 4개 카테고리에 각 10개 시드 키워드. 로테이션 기반으로 주제 선정 |
| `repo-tracker.yml` | GitHub 레포별 회고 상태 추적. SHA 비교로 변경 감지 |

초기에는 데이터 파일 없이 운영했는데, 4일간 24개 포스트를 발행하면서 주제 겹침과 레포 추적이 필요해졌다. 데이터 파일은 하네스가 상태를 기억하는 장치다.

### write-post 스킬 업그레이드

front matter에 `mermaid: true`, `chart: true`, `math: true` 옵션을 추가했다. 글 내용에 따라 Mermaid 다이어그램, Chart.js 차트, KaTeX 수식을 삽입할 수 있다. Jekyll 빌드 시 해당 라이브러리를 조건부로 로드한다.

### 권한 모델 변경

초기에는 허용 목록(allow list) 8개를 지정했다. auto-publish 파이프라인이 추가되면서 git push, Skill 호출 등 더 많은 도구가 필요해졌다. 허용 목록을 유지하면 새 기능을 추가할 때마다 목록을 수정해야 한다.

`bypassPermissions` 모드로 전환하고, 차단 목록 3개만 유지하는 방식으로 바꿨다. `rm -rf`, `git push --force`, `git reset --hard`만 차단한다. 나머지는 전부 허용한다.

### 4일간 운영 결과

- 발행 포스트: 24개 (6개 카테고리)
- 리뷰 1차 통과: 거의 없음. 24개 중 1차에서 바로 합격한 건은 2-3건 수준이다
- 빌드 실패로 중단: 0건

리뷰 불합격 사유는 링크 텍스트 규칙 위반(source-policy), 빈 수식어 사용(blacklist), 1인칭 관점 부재(tone) 순이었다. 이 패턴이 반복되어 writer 에이전트 프롬프트에 블랙리스트 항목과 1인칭 시점 강조 문구를 추가했다.
