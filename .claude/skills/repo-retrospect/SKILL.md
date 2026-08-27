---
name: repo-retrospect
description: GitHub 레포(public/private)를 분석하여 프로젝트 회고 포스트 작성. 신규 레포는 새 포스트, 변경된 레포는 업데이트
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash, Skill
---

# 프로젝트 회고 자동 발행

## 프로세스

### 1단계: 레포 상태 점검
1. GitHub API로 dorec9의 레포 목록을 조회한다 (private 포함).
   `user/repos`는 인증된 사용자 기준이라 private까지 나온다 — `users/dorec9/repos`(public만)와 다르다:
   ```bash
   gh api "user/repos?per_page=100&affiliation=owner" --paginate \
     --jq '.[] | {name, description, language, pushed_at, default_branch, visibility, created_at}'
   ```
   private이 하나도 안 나오면 토큰 권한 부족이다 — 5단계 "권한 부족 시" 항목을 따른다
2. `_data/repo-tracker.yml`을 읽는다
3. **회고 대상 제외 기준** — `_data/repo-tracker.yml`의 `excluded` 목록에 있으면 건너뛴다.
   목록에 없어도 아래에 해당하면 제외하고, 제외 사유를 한 줄 남긴다.
   **판단이 애매하면 제외한다** — 공개 블로그에 나가고 검색엔진에 색인되는 글이다:
   - 서버·인프라 운영 레포: 배포 설정, docker-compose/k8s 매니페스트, nginx·CI 설정,
     VPS·홈서버 구성, 도메인/인증서 관리
   - 개인 사이트·블로그 레포 (dorec9.github.io 포함)
   - dotfiles, 개인 설정, 스크립트 모음
   - 자격증명이 얽힌 레포: .env에 실제 값이 커밋돼 있거나 히스토리에 키/토큰 흔적이 있는 경우
   - 포크이거나 본인 기여를 특정할 수 없는 레포 (수업 팀 레포에서 남의 코드 비중이 큰 경우 등)
   제외한 레포는 `repo-tracker.yml`에 `status: "excluded"`와 사유를 기록해 매번 재판단하지 않는다
4. 다음 우선순위로 대상 레포 1개를 선택한다:
   - a) `status: "not_covered"` — 아직 회고하지 않은 레포 (우선)
   - b) `status: "published"` + GitHub의 최신 커밋 SHA가 `last_sha`와 다른 레포 (변경 발생)
5. 선택 대상이 없으면 "이번 주 회고 대상 없음"을 출력하고 **종료**

### 2단계: 레포 심층 분석
회고는 프로젝트의 **전체 흐름**을 다룬다. 최근 커밋 몇 개만 보면 끝자락만 쓰게 되므로
커밋 이력을 충분히 확보한다.

1. README 내용:
   ```bash
   gh api repos/dorec9/{repo}/readme --jq '.content' | base64 -d
   ```
2. 커밋 이력 — 최근 200개까지 (제목 줄만, 프로젝트 흐름 파악용):
   ```bash
   gh api "repos/dorec9/{repo}/commits?per_page=100" --paginate \
     --jq '.[] | "\(.commit.author.date[0:10]) \(.sha[0:7]) \(.commit.message | split("\n")[0])"' \
     | head -200
   ```
3. 총 커밋 수와 프로젝트 기간 (회고에 쓸 규모 감각):
   ```bash
   gh api "repos/dorec9/{repo}/contributors?per_page=100" --jq '[.[].contributions] | add'
   gh api repos/dorec9/{repo} --jq '{created_at, pushed_at, size, visibility}'
   ```
4. 설계 판단이 드러나는 커밋 5~10개를 골라 실제 diff를 본다
   (리팩터링·아키텍처 변경·버그 수정 커밋 우선):
   ```bash
   gh api repos/dorec9/{repo}/commits/{sha} --jq '.files[] | {filename, additions, deletions}'
   ```
5. 사용 언어:
   ```bash
   gh api repos/dorec9/{repo}/languages
   ```
6. 디렉토리 구조:
   ```bash
   gh api repos/dorec9/{repo}/git/trees/{default_branch}?recursive=1 --jq '.tree[] | .path'
   ```

**업데이트 대상(status: published + SHA 변경)인 경우**는 최근 N개가 아니라
`last_sha` 이후 커밋만 정확히 가져온다:
```bash
gh api "repos/dorec9/{repo}/compare/{last_sha}...{default_branch}" \
  --jq '{ahead: .ahead_by, commits: [.commits[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"]}'
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

## 본문에 쓰지 않는 것
private 레포도 회고 대상이므로, 레포에서 읽은 내용 중 아래는 본문에 옮기지 않는다.
글은 공개되고 검색엔진에 색인된다:
- 서버 주소, 내부 호스트명, 포트, IP, 도메인 관리 정보
- API 키·토큰·비밀번호·인증서, .env의 실제 값 (예시 형식만 쓴다)
- 비공개 API 엔드포인트 전체 경로, DB 스키마의 실제 접속 정보
- 본인 외 팀원의 실명·이메일·계정 (커밋 author 정보 포함)
- 클라이언트·회사명이 드러나는 식별 정보 (NDA 가능성)

기술 스택과 설계 판단은 쓰되, 그걸 그대로 재현할 수 있는 운영 정보는 뺀다.
설계 판단을 설명하는 데 위 정보가 꼭 필요하면, 그 레포는 회고 대상에서 제외한다.
