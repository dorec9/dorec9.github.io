---
title: "컴퓨터를 꺼야 멈추던 자동 발행, GitHub Actions로 부활시킨 과정"
date: 2026-07-29
categories: harness-engineering
tags: [GitHub-Actions, Claude-Code, 블로그자동화, cron, CI/CD, OAuth, 하네스엔지니어링]
excerpt: "tmux 상시 실행이 전제였던 자동 발행을 접었다가 GitHub Actions cron으로 되살렸다. 방식 비교, 요일 로테이션 설계, 인증에서 막힌 2가지를 기록한다."
---

## 왜 접었고, 왜 다시 시작했나

[초기 하네스]({% post_url 2026-04-02-claude-code-blog-harness-setup %})는 리눅스에서 tmux로 Claude Code REPL을 상시 실행하는 구조였다. REPL 안의 cron이 하루 4개 카테고리를 발행했다. 문제는 전제 조건이었다. 컴퓨터를 끄면 발행이 멈춘다. 결국 운영을 접었다.

이번에 작업 환경을 윈도우로 옮기면서 구조를 다시 설계했다. 목표는 하나였다. 내 컴퓨터의 전원 상태와 발행 스케줄을 분리하는 것.

---

## 두 가지 선택지

로컬 상시 실행 없이 스케줄을 돌리는 방법으로 2가지를 검토했다.

| 기준 | 클라우드 예약 에이전트 | GitHub Actions cron |
|------|----------------------|---------------------|
| 세팅 | 채팅에서 바로 등록 | 워크플로우 YAML 작성 |
| 실행 위치 | Anthropic 클라우드 | GitHub 러너 |
| 저장소와의 관계 | 저장소 밖에 존재 | 저장소 안에서 버전 관리 |
| 실행 로그 | 제품 안에서 확인 | Actions 탭에 전체 보존 |
| 비용 | 구독 플랜 사용량 | public repo 러너 무료 + 구독 플랜 사용량 |

GitHub Actions를 선택했다. 결정 기준은 완결성이다. 이 저장소는 하네스 엔지니어링을 보여주는 공간인데, 스케줄러가 저장소 밖에 있으면 구조의 절반이 보이지 않는다. 워크플로우 파일까지 저장소 안에 있어야 규칙, 스킬, 훅, 스케줄러가 하나의 코드베이스로 완결된다.

---

## 요일 로테이션 설계

기존에는 평일 하루 4개를 발행했다. 5일간 24개가 쌓였는데, 되돌아보니 밀도가 과했다. 부활하면서 하루 1개로 줄였다.

줄이고 나니 시간표가 맞아떨어졌다. 평일 5일 = 주간 레포 회고 1개 + 카테고리 4개.

| 요일 | 작업 |
|------|------|
| 월 | `/repo-retrospect` — GitHub 레포 분석 회고 |
| 화 | `/auto-publish planning-insight` |
| 수 | `/auto-publish data-statistics` |
| 목 | `/auto-publish trend-research` |
| 금 | `/auto-publish business-economy` |

실행 시각은 09:17 KST로 정했다. 근거는 2가지다. 첫째, GitHub Actions의 cron은 UTC 기준이다. KST 오전 9시 이후로 잡으면 UTC와 날짜가 같아져 요일 계산이 단순해진다(09:17 KST = 00:17 UTC). 둘째, 정각을 피했다. 스케줄 이벤트는 정각에 수요가 몰려 지연될 수 있다([GitHub 공식 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)도 고부하 시간대의 지연 가능성을 명시한다).

요일 분기는 cron 표현식 5개를 등록하는 대신, 러너 안에서 `TZ=Asia/Seoul date +%u`로 처리했다. 유지할 스케줄이 1개로 줄어든다.

---

## 윈도우 이전에서 고친 3가지

리눅스 전제가 저장소 곳곳에 박혀 있었다. 옮기면서 셋을 고쳤다.

1. **가짜 python3.** 윈도우의 `python3`는 Microsoft Store 설치를 안내하는 스텁 실행 파일이다. 이 때문에 front matter 검증 훅이 오류 메시지도 없이 무력화되어 있었다. 실행 가능 여부를 검사한 뒤 `python3 → python → py` 순서로 폴백하도록 고쳤다.
2. **CRLF 변환.** Git for Windows의 기본값 `core.autocrlf=true`는 체크아웃 때 줄바꿈을 CRLF로 바꾼다. bash 스크립트에 CR이 섞이면 실행이 깨진다. `.gitattributes`에 `*.sh text eol=lf`를 고정해서 차단했다.
3. **훅 경로 문법.** 윈도우에서 훅 명령은 cmd로 실행되어 `$CLAUDE_PROJECT_DIR` 같은 셸 변수가 확장되지 않는다. 훅 로직을 전부 `.sh` 파일로 옮기고, 호출을 상대경로 `bash .claude/hooks/...`로 통일했다. 이 형태는 윈도우 cmd와 리눅스 sh 양쪽에서 동작해서, 같은 설정이 GitHub Actions 러너에서도 그대로 쓰인다.

빌드 검증 훅에는 조건을 하나 추가했다. Ruby가 없는 환경이면 조용히 건너뛴다. 대신 Actions 러너에는 Ruby를 설치해서, push 전 Jekyll 빌드 게이트가 CI에서는 항상 동작하게 했다. 로컬은 가볍게, CI는 엄격하게 가져가는 구성이다.

---

## 인증에서 막힌 2가지

**1. GitHub App 토큰 교환 실패.** 실행 주체인 [claude-code-action](https://github.com/anthropics/claude-code-action)은 `github_token` 입력이 없으면 Claude GitHub App의 OIDC 토큰 교환을 시도한다. 앱을 설치하지 않은 저장소에서는 이 단계가 실패한다. 워크플로우에 `github_token: ${{ "{{" }} github.token {{ "}}" }}`을 명시해서 교환 자체를 건너뛰었다.

**2. 인증 코드를 토큰으로 착각.** 구독 인증용 토큰은 `claude setup-token`으로 발급한다. 절차는 브라우저 승인 → 인증 코드 표시 → 코드를 터미널에 입력 → 토큰 출력 순서다. 나는 중간 산출물인 인증 코드를 최종 토큰으로 착각해 secret에 등록했다. 실행은 2초 만에 비용 $0으로 종료됐다. 구분법은 접두사다. 토큰은 `sk-ant-oat01-`로 시작한다. 이 접두사가 없으면 토큰이 아니다.

두 실패의 공통점이 있다. 값이 아니라 절차의 문제였다. 오류 메시지를 따라가며 값을 의심하기 전에, 절차를 끝까지 완료했는지부터 확인해야 했다.

---

## 검증 결과

수정 후 첫 실행에서 파이프라인 전체가 통과했다.

- 수요일 카테고리(data-statistics)가 요일 분기로 선택됐다
- 시드 키워드 중 미사용 주제(이상치 탐지)를 골랐다
- 리서치 → 작성 → 리뷰 → Jekyll 빌드 검증 → 커밋 → push까지 완료됐다
- GITHUB_TOKEN으로 push한 커밋이 GitHub Pages 배포를 트리거하는 것도 확인했다

마지막 항목은 사전에 확신이 없던 부분이다. GITHUB_TOKEN의 push는 다른 워크플로우를 트리거하지 않는 것이 기본 동작인데([GitHub 공식 문서](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)), Pages 빌드는 별도 파이프라인이라 정상 동작했다. 이 성질 덕분에 발행 커밋이 auto-publish를 재귀 호출하는 무한 루프도 구조적으로 발생하지 않는다.

---

## 배운 점

1. **스케줄러는 저장소 안에 있어야 한다.** 하네스 구성 요소가 저장소 밖에 있으면 재현하기도, 증명하기도 어렵다.
2. **인증 실패의 절반은 절차 문제다.** 발급 절차의 마지막 단계까지 완료했는지가 토큰 값 자체보다 먼저 확인할 항목이다.
3. **발행 빈도는 시스템 성능이 아니라 편집 판단이다.** 하루 4개를 돌릴 수 있어도, 돌려야 하는 것은 아니다.

다음 단계는 운영 데이터 축적이다. Actions 로그에 남는 리뷰 불합격 사유를 모아서, 반복 패턴을 `failures/registry.md`를 거쳐 규칙으로 승격시키는 루프를 돌릴 계획이다.
