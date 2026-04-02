---
name: repo-retrospect
description: GitHub public 레포를 분석하여 프로젝트 회고 포스트 작성. 신규 레포는 새 포스트, 변경된 레포는 업데이트
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash, Skill
---

# 프로젝트 회고 자동 발행

## 프로세스

### 1단계: 레포 상태 점검
1. GitHub API로 dorec9의 public 레포 목록을 조회한다:
   ```bash
   gh api users/dorec9/repos --jq '.[] | {name, description, language, pushed_at, default_branch}'
   ```
2. `_data/repo-tracker.yml`을 읽는다
3. `excluded` 목록의 레포(dorec9.github.io 등)는 건너뛴다
4. 다음 우선순위로 대상 레포 1개를 선택한다:
   - a) `status: "not_covered"` — 아직 회고하지 않은 레포 (우선)
   - b) `status: "published"` + GitHub의 최신 커밋 SHA가 `last_sha`와 다른 레포 (변경 발생)
5. 선택 대상이 없으면 "이번 주 회고 대상 없음"을 출력하고 **종료**

### 2단계: 레포 심층 분석
선택한 레포에 대해 다음 정보를 수집한다:
1. README 내용:
   ```bash
   gh api repos/dorec9/{repo}/readme --jq '.content' | base64 -d
   ```
2. 최근 커밋 10개:
   ```bash
   gh api repos/dorec9/{repo}/commits?per_page=10
   ```
3. 사용 언어:
   ```bash
   gh api repos/dorec9/{repo}/languages
   ```
4. 디렉토리 구조:
   ```bash
   gh api repos/dorec9/{repo}/git/trees/{default_branch}?recursive=1 --jq '.tree[] | .path'
   ```

### 3단계: 포스트 작성

**신규 레포인 경우 (not_covered):**
- `/write-post` 스킬로 포스트 생성
- 카테고리: `project-retrospect`
- 구조:
  - 프로젝트 배경과 목적
  - 기술 스택과 선택 이유
  - 핵심 설계 판단
  - 배운 점과 개선할 점

**기존 레포 업데이트인 경우 (published + 변경 발생):**
- 기존 포스트 파일을 `_posts/`에서 찾는다 (repo-tracker.yml의 post_slug 참조)
- 변경 내용(새 커밋들)을 분석한다
- 기존 포스트 본문 하단에 `## YYYY-MM-DD 업데이트` 섹션을 추가한다
- front matter의 `date`는 원본 유지 (URL 변경 방지)
- 새 기술 키워드가 있으면 `tags`에 추가

### 4단계: 리뷰
- `/review-post` 스킬로 품질 검증
- 불합격 시: 수정 후 재리뷰 (최대 2회)
- 3회 불합격 시: `failures/registry.md`에 기록하고 중단

### 5단계: 트래커 갱신
`_data/repo-tracker.yml` 업데이트:
- **신규:** status를 `published`로 변경, last_sha, last_post_date, post_slug 기록
- **업데이트:** last_sha와 last_post_date 갱신

### 6단계: 히스토리 갱신
`_data/topic-history.yml`의 `project-retrospect`에 엔트리 추가:
```yaml
- slug: "{repo-slug}-retrospect"
  date: "YYYY-MM-DD"
  title: "포스트 제목"
  repo: "dorec9/{repo}"
  sha: "{latest_sha}"
```

### 7단계: 발행
1. `bundle exec jekyll build`로 빌드 검증
2. 빌드 실패 시 중단
3. 빌드 성공 시:
   - `git add _posts/ _data/`
   - `git commit -m "글 발행: {repo} 프로젝트 회고"`
   - `git push origin main`
4. 커밋 메시지에 Co-Authored-By 절대 넣지 않는다

## 규칙
- `.claude/rules/`의 tone, blacklist, source-policy 규칙 필수 준수
- push는 사용자 확인 없이 자동 실행
- force push 절대 불가
- dorec9.github.io 레포는 절대 회고 대상에 포함하지 않는다
