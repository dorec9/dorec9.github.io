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
   조회 결과가 0건이거나 private이 하나도 안 나오면 토큰 권한 문제일 수 있다 —
   아래 "조회 결과 기록"을 반드시 수행한다
2. `_data/repo-tracker.yml`을 읽는다
3. **회고 대상 제외 기준** — `_data/repo-tracker.yml`의 `excluded` 목록에 있으면 건너뛴다.
   목록에 없어도 아래는 회고 재료로 부적합하니 제외하고, 사유를 한 줄 남긴다:
   - dorec9.github.io (이 블로그 자신)
   - 자격증명이 얽힌 레포: .env에 실제 값이 커밋돼 있거나 히스토리에 키/토큰 흔적이 있는 경우
   - 포크이거나 본인 기여를 특정할 수 없는 레포 (수업 팀 레포에서 남의 코드 비중이 큰 경우 등)
   - dotfiles·개인 설정 모음처럼 설계 판단을 서술할 내용이 없는 레포

   서버·인프라 운영 레포나 개인 사이트 레포도 **회고 자체는 가능하다.**
   단 아래 "본문에 쓰지 않는 것"을 반드시 지킨다 — 구조와 판단은 쓰되 주소는 쓰지 않는다.
   제외한 레포는 `repo-tracker.yml`에 `status: "excluded"`와 사유를 기록해 매번 재판단하지 않는다
4. 다음 우선순위로 대상 레포 1개를 선택한다:
   - a) `status: "not_covered"` — 아직 회고하지 않은 레포 (우선)
   - b) `status: "published"` + GitHub의 최신 커밋 SHA가 `last_sha`와 다른 레포 (변경 발생)
5. **조회 결과 기록 (필수)** — 회고를 하든 안 하든 무슨 일이 있었는지 흔적을 남긴다.
   월요일은 무발행이 정상일 수 있어 워크플로우 검증에서 예외 처리되므로,
   이 기록이 없으면 "신규 레포 없음"과 "토큰이 죽어 아무것도 못 봄"이 구분되지 않는다:
   ```bash
   {
     echo "## repo-retrospect 조회 결과"
     echo "- 조회된 레포: ${TOTAL}개 (public ${PUB} / private ${PRIV})"
     echo "- 제외: ${EXCLUDED}개"
     echo "- 회고 대상: ${TARGET:-없음}"
     [ "$PRIV" -eq 0 ] && echo "- ⚠️ private 레포 0건 — REPO_SCAN_TOKEN 미설정/만료 가능성"
   } >> "${GITHUB_STEP_SUMMARY:-/dev/stdout}"
   ```
6. 선택 대상이 없으면 위 기록을 남긴 뒤 "이번 주 회고 대상 없음"을 출력하고 **종료**.
   단 private이 0건으로 나왔다면 정상 종료가 아니다 —
   `failures/registry.md`에 토큰 문제로 기록하고 그 기록을 커밋·push한다

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

## 본문에 쓰지 않는 것 (YOU MUST NOT)
레포는 자유롭게 읽되, 읽은 것 중 아래는 본문에 옮기지 않는다.
글은 공개되고 검색엔진에 색인된다.

**1순위 — 운영자의 사이트·서버 주소**
- 본인이 운영하는 개인 사이트·서비스의 도메인, URL, 접속 주소
- 서버 IP, 내부 호스트명, 포트, VPS·홈서버 위치, 도메인/DNS 관리 정보
- 배포 대상 주소가 드러나는 설정값 (nginx server_name, 배포 스크립트의 호스트 등)

이 블로그(dorec9.github.io)와 GitHub 프로필 링크는 예외 — 그건 공개된 신원이다.
그 외에 운영자가 따로 굴리는 사이트 주소는 이 블로그에 노출하지 않는다.

**2순위 — 자격증명과 타인 정보**
- API 키·토큰·비밀번호·인증서, .env의 실제 값 (예시 형식만 쓴다)
- 비공개 API 엔드포인트 전체 경로, DB 실제 접속 정보
- 본인 외 팀원의 실명·이메일·계정 (커밋 author 정보 포함)
- 클라이언트·회사명이 드러나는 식별 정보 (NDA 가능성)

**원칙**: 아키텍처·기술 스택·설계 판단은 쓴다. 그걸 실제로 찾아가거나 접속할 수 있는
주소·자격증명은 뺀다. "Nginx 리버스 프록시로 3개 서비스를 라우팅했다"는 쓰고,
그 도메인이 뭔지는 쓰지 않는다.

작성 후 발행 전에 본문을 다시 훑어 위 항목이 남아 있는지 확인한다.
