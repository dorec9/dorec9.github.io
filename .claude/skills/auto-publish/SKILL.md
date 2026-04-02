---
name: auto-publish
description: 지정 카테고리의 자동 발행 파이프라인. 주제 선정 → 리서치 → 작성 → 리뷰 → 발행까지 일괄 실행
argument-hint: [카테고리slug]
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash, Skill
---

# 자동 발행 파이프라인

## 입력
- `$ARGUMENTS`: 카테고리 slug (planning-insight | data-statistics | trend-research | business-economy)

## 프로세스

### 1단계: 주제 선정
1. `_data/topic-history.yml`을 읽어 **전체 카테고리**의 기존 발행 목록을 확인한다
2. `_data/seed-keywords.yml`에서 해당 카테고리의 시드 키워드를 읽는다
3. 기존 발행된 slug/title/keywords와 겹치지 않는 시드 키워드 1개를 선택한다
4. WebSearch로 선택한 키워드의 최신 동향을 파악한다
5. 구체적이고 겹치지 않는 포스트 주제 1개를 확정한다

### 2단계: 리서치
- 확정된 주제로 `/research` 스킬 실행
- Tier 1/2 소스 최소 3개 확보

### 3단계: 작성
- `/write-post` 스킬로 포스트 생성
- 카테고리는 `$ARGUMENTS`로 전달받은 slug 사용
- 리서치 결과를 근거로 활용

### 4단계: 리뷰
- `/review-post` 스킬로 품질 검증
- 불합격 시: 피드백 반영하여 수정 후 재리뷰 (최대 2회 반복)
- 3회 연속 불합격 시: `failures/registry.md`에 기록하고 **중단**

### 5단계: 히스토리 갱신
- `_data/topic-history.yml`의 해당 카테고리에 새 엔트리 추가:
  ```yaml
  - slug: "파일명-slug"
    date: "YYYY-MM-DD"
    title: "포스트 제목"
    keywords: [사용된 키워드들]
  ```

### 6단계: 발행
1. `bundle exec jekyll build`로 빌드 검증
2. 빌드 실패 시 **중단** + `failures/registry.md`에 기록
3. 빌드 성공 시:
   - `git add _posts/ _data/topic-history.yml`
   - `git commit -m "글 발행: [포스트 제목]"`
   - `git push origin main`
4. 커밋 메시지에 Co-Authored-By 절대 넣지 않는다

## 규칙
- `.claude/rules/`의 tone, blacklist, source-policy, topic-policy 규칙 필수 준수
- 카테고리 간 교차 중복도 방지 (다른 카테고리에서 이미 다룬 주제 피하기)
- push는 사용자 확인 없이 자동 실행 (빌드 성공 조건만 체크)
- force push 절대 불가
