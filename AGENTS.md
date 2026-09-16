# Codex 블로그 자동 발행 지침

## 프로젝트

- 경영기획·IT기획 직무를 위한 Jekyll 기술 블로그다.
- 기본 응답, 글, 커밋 메시지는 한국어로 작성한다.
- 발행 대상은 `main` 브랜치이며 GitHub Pages가 배포한다.
- 사용자가 자동 발행과 대기열 처리를 승인했다. 정상 검증을 통과한 포스트는 별도 확인 없이 커밋하고 push한다.
- force push, 기존 포스트 삭제, 사용자 변경 되돌리기는 금지한다.

## 작업 시작

1. `git status --short`로 사용자 변경을 확인한다. 겹치는 변경은 건드리지 않는다.
2. `git pull --ff-only origin main`으로 원격과 동기화한다.
3. `README.md`, `_data/topic-history.yml`, `_data/seed-keywords.yml`을 읽는다.
4. `.claude/rules/`의 `tone.md`, `blacklist.md`, `source-policy.md`, `topic-policy.md`를 품질 규칙으로 사용한다. 폴더 이름은 과거 이력일 뿐 Claude 실행을 요구하지 않는다.

## 대기열 처리

`_data/publish-backlog.yml`에서 `status: pending`인 가장 오래된 항목 하나만 처리한다.

1. 항목의 `date`, `category`, `topic`을 사용한다.
2. `project-retrospect` 항목은 `repo`가 지정되어 있으면 그 저장소를 분석한다. 비공개 저장소 내용을 다룰 때 자격증명, 서비스 주소, 타인 정보는 공개하지 않는다.
3. 최신성이 중요한 주장과 수치는 현재 웹 자료로 확인한다. 공식 문서·정부 통계·학술 논문·기업 공시를 우선한다.
4. 기존 이력과 겹치면 같은 카테고리의 미사용 시드에서 대체 주제를 고르고 대기열의 `topic`을 갱신한다.
5. `_posts/YYYY-MM-DD-slug.md`에 1,500~3,000자 분량으로 작성한다. 최소 3개의 Tier 1·2 출처를 본문 주장 가까이에 링크한다.
6. `_data/topic-history.yml`에 slug, date, title, keywords를 추가한다. 회고 글은 repo와 SHA도 기록한다.
7. 대기열 항목을 `status: published`로 바꾸고 `post`에 파일명을 기록한다.
8. `python scripts/validate_post.py <포스트 경로>`와 `bundle exec jekyll build`를 실행한다. Ruby/Bundler가 없으면 그 사실을 기록하되, 포스트 검증은 생략하지 않는다.
9. 검증 실패는 두 번까지 수정한다. 해결하지 못하면 `status: failed`와 `failure_reason`을 기록하고, 글 파일과 히스토리 변경은 커밋하지 않는다.
10. 검증 성공 시 포스트, 히스토리, 대기열과 필요한 이미지 파일만 명시적으로 stage한다. `글 발행: <제목>`으로 커밋하고 `git push origin main`을 실행한다.
11. push 후 원격 커밋과 GitHub Pages 배포 상태를 확인한다.

한 실행에서 두 편 이상 발행하지 않는다. 대기열이 비면 새 글을 만들지 말고 완료 상태만 보고한다.

## 글 규칙

- 문체는 `~다` 체이며 실무자 관점으로 쓴다.
- 구체적 수치와 사례를 먼저 제시하고 판단 근거를 설명한다.
- 기술 용어는 처음 나올 때 한 문장으로 설명한다.
- front matter에는 `title`, `date`, `categories`, `tags`, `excerpt`가 모두 있어야 한다.
- 파일 날짜와 front matter 날짜는 대기열 날짜와 일치해야 한다.
- 과장 표현과 AI 특유 표현은 `.claude/rules/blacklist.md`에 따라 금지한다.
- 생성 AI 출력, 출처 불명 데이터, 커뮤니티 루머를 근거로 사용하지 않는다.
- 운영 중인 개인 서비스 주소, IP, 내부 호스트명, 포트, 토큰, 이메일, 타인 실명은 공개하지 않는다.
- 기존 A/B 실험의 목록 UI, excerpt 표시 코드, GA 코드는 변경하지 않는다.

## 대외 공개 원칙

- 포스트는 독자를 설득하고 정보를 전달하는 완성된 결과물로 쓴다.
- 대기열, 누락분, 밀린 글, 자동화 장애, 복구 작업, 재시도 횟수 등 내부 운영 사정을 본문에 쓰지 않는다.
- 예약된 게시 날짜와 실제 작성일이 다르다는 사실을 본문에서 설명하지 않는다.
- `자료는 YYYY-MM-DD에 확인했다`처럼 작성 과정을 노출하는 메타 문구를 넣지 않는다. 자료의 연도가 주장 해석에 필요할 때만 자연스럽게 밝힌다.
- 프로젝트 회고에서 문제를 다뤄야 할 때는 해결 능력과 설계 판단을 보여주는 사례만 선별한다. 현재 운영상의 약점이나 불필요한 자기비하는 공개하지 않는다.
- 사실을 꾸미거나 출처 시점을 왜곡하지 않는다. 공개할 필요가 없는 내부 사정만 생략한다.

## 정기 발행

대기열 완료 후 정기 발행을 다시 시작할 때도 한 실행에 한 편만 발행한다.

- 월: `project-retrospect`
- 화: `planning-insight`
- 수: `data-statistics`
- 목: `trend-research`
- 금: `business-economy`

동일 KST 날짜의 포스트가 이미 있으면 중복 발행하지 않는다. 월요일에 회고할 변경 저장소가 없으면 무발행을 정상으로 기록한다.
