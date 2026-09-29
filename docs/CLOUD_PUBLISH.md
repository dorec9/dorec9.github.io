# PC 없이 발행하는 설정

현재 정기 발행은 로컬 Codex 예약 작업이므로 PC와 앱이 실행 중이어야 한다. `.github/workflows/auto-publish-cloud.yml`은 GitHub 호스팅 실행기에서 평일 09:17 KST에 작동하도록 준비됐다. 저장소 변수 `AUTO_PUBLISH_CLOUD_ENABLED=true`가 설정되기 전에는 실행하지 않는다.

## 활성화 순서

1. OpenAI API Platform에서 별도 결제 수단과 사용 한도를 설정한다. ChatGPT Pro 구독은 API 사용료를 포함하지 않는다.
2. OpenAI API 키를 발급해 GitHub 저장소 **Settings → Secrets and variables → Actions → Repository secrets**의 `OPENAI_API_KEY`로 저장한다. 키를 저장소 파일, 이슈, 채팅에 입력하지 않는다.
3. 저장소 변수 `AUTO_PUBLISH_CLOUD_ENABLED`를 `true`로 설정한다.
4. Actions에서 **클라우드 자동 발행**을 수동 실행하고 새 글 한 편, 발행 커밋, Pages 빌드, 실제 글 URL을 확인한다. 이미 오늘 글이 있다면 중복 방지로 건너뛰므로 다음 미발행 평일에 시험한다.
5. 클라우드 발행이 확인되면 로컬 `dorec9 평일 블로그 정기 발행` 자동화를 중지한다. 두 일정이 동시에 돌지 않게 한다.

워크플로는 새 포스트 한 편과 발행 이력만 허용하고, `validate_post.py` 및 Jekyll 빌드를 통과한 뒤 커밋한다. GitHub Actions의 `GITHUB_TOKEN`으로 push한 커밋은 브랜치 기반 Pages 빌드를 자동으로 일으키지 않으므로 Pages 빌드를 별도로 요청하고 게시된 URL까지 확인한다. 실패하면 실행 로그 링크가 담긴 이슈를 만든다.

일정 실행은 GitHub 측 부하에 따라 예약 시각보다 늦어지거나 드물게 누락될 수 있다. 공개 저장소가 60일 동안 활동이 없으면 GitHub가 예약 워크플로를 비활성화할 수도 있다. 이를 운영할 때는 Actions 실행 내역과 실패 이슈를 함께 확인한다.
