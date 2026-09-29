이 저장소의 AGENTS.md, README.md, `.claude/rules/` 네 규칙, `_data/topic-history.yml`, `_data/seed-keywords.yml`을 먼저 읽는다.

현재 KST 날짜의 요일에 맞는 새 글 한 편만 작성한다. 월요일은 project-retrospect, 화요일은 planning-insight, 수요일은 data-statistics, 목요일은 trend-research, 금요일은 business-economy다. 같은 날짜의 글이 이미 있으면 아무 파일도 고치지 않는다. 월요일에는 공개 가능한 변경 저장소가 없으면 아무 글도 만들지 않는다.

주제와 주장에 필요한 최신 공식 문서, 논문, 공공기관 자료를 직접 확인한다. 검색 결과 요약만 근거로 사용하지 않는다. 근거를 직접 확인할 수 없다면 글을 만들지 않고 이유를 최종 메시지에 남긴다. 이전 주제와 겹치지 않는 실무적 주제를 고른다. 시각 자료는 글의 핵심을 실제로 설명하는 표, Mermaid, 그래프, 수식 중에서 판단한다. 내부 자동화 사정과 작성 과정은 공개 글에 쓰지 않는다.

새 포스트와 `_data/topic-history.yml`만 수정한다. 회고 글에서 필요한 경우에만 `_data/repo-tracker.yml`도 수정한다. 자격증명과 개인 서비스 주소를 노출하지 않는다. 이 실행 안에서는 Git commit 또는 push를 하지 않는다. 뒤의 워크플로 단계가 파일을 검사한 뒤 커밋한다.
