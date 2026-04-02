# 주제 선정 규칙

## 필수 참조
- 포스트 작성 전 반드시 `_data/topic-history.yml`을 읽어 기존 발행 이력을 확인한다
- 기존 slug, title, keywords와 겹치는 주제는 선택하지 않는다

## 중복 방지
- 동일 카테고리 내 중복 금지
- 카테고리 간 교차 중복도 방지 (예: trend-research에서 다룬 주제를 planning-insight에서 반복하지 않는다)
- 유사 주제는 다른 관점/깊이로 차별화할 수 있으면 허용

## 시드 키워드 로테이션
- `_data/seed-keywords.yml`에서 해당 카테고리의 키워드를 참조한다
- 최근 사용하지 않은 키워드를 우선 선택한다
- 시드 키워드는 출발점일 뿐, 최신 동향에 맞게 구체화한다

## 히스토리 기록
- 포스트 발행 후 반드시 `_data/topic-history.yml`에 기록한다
- slug, date, title, keywords를 모두 포함한다
