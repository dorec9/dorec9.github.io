---
title: "키움증권 자동매매 시스템을 만든 과정 — 32bit/64bit 프로세스 분리와 랜덤 100회 벤치마크"
date: 2026-08-17
categories: [project-retrospect]
tags: [Python, FastAPI, PyQt5, 키움증권, OpenAPI+, scikit-learn, PostgreSQL, websockets, 자동매매, 백테스트]
excerpt: "키움증권 REST API와 구형 OpenAPI+를 함께 쓰는 자동매매 시스템을 개인 프로젝트로 만들었다. 32bit COM 제약을 프로세스 분리로 풀어낸 판단, 모델을 랜덤 100회 시행과 비교하는 벤치마크 설계, 그 과정에서 만난 회계·타임존 버그를 정리한다."
---

키움증권 자동매매를 만들려고 보니 API가 두 개였다. REST API는 최신이지만 조건검색 같은 일부 기능이 안 되고, 구형 OpenAPI+는 조건검색까지 되지만 32bit Windows COM 전용이다. 이 둘을 한 시스템 안에 어떻게 넣을지가 이번 프로젝트(seedagent)의 핵심 문제였다.

---

## 배경

2026년 6월 23일부터 7월 3일까지 PR 16개를 거쳐 인증 모듈에서 조건검색 통합까지 진행했다. README에는 "현재 단계에서는 인증 모듈만 구현했다"고 적혀 있지만, 실제 커밋 히스토리는 시세조회 → 수집기 → DB 저장 → 룰 기반 시그널 → ML 모델 → 백테스트 → 벤치마크 → 조건검색까지 이어졌다. README 업데이트가 코드 진행 속도를 따라가지 못한 상태로 남아 있다.

---

## 핵심 설계 판단 — 32bit/64bit 프로세스 분리

가장 오래 고민한 부분이다. 키움 OpenAPI+는 Windows COM/OCX 컨트롤이라 32bit Python에서만 동작한다. 반면 scikit-learn·pandas 기반 ML 파이프라인과 FastAPI 서버는 64bit로 돌리는 게 안정적이다. 하나의 프로세스에 두 요구사항을 다 넣을 수 없었다.

그래서 두 프로세스로 나눴다. `client/main.py`와 `client/kiwoom_api.py`가 "32bit 실행 노드"다. PyQt5 `QApplication` 이벤트 루프에서 Kiwoom OCX 콜백을 받는다. 대상은 `on_tr_data`, `on_real_data`, `on_chejan_data`, `on_login`이다. COM 이벤트는 자체 메시지 루프가 필요해서 QApplication 없이는 콜백이 오지 않는다. `server/`는 "64bit 브레인 서버"로 FastAPI가 담당한다.

둘 사이는 `client/ws_client.py`의 `KiwoomWSClient`가 `ws://localhost:8000/ws/kiwoom`으로 연결한다. 64bit 서버가 `comm_rq_data`, `send_order` 등 명령을 내린다. 32bit 노드가 이를 실행하고 결과를 이벤트로 돌려준다. 조건검색은 32bit 노드가 `ws://127.0.0.1:8765`로 별도 로컬 서버를 연다. "load_condition" 명령을 받으면 키움 서버에서 조건식 목록을 가져와 응답하는 방식으로 검증했다(`test_condition.py`).

프로세스를 나누면 통신 지연과 직렬화 비용이 생긴다. 그래도 32bit COM 제약과 64bit ML 스택을 한 프로세스에 억지로 맞추는 것보다는, 역할을 명확히 나누고 websocket으로 연결하는 쪽이 유지보수 관점에서 나은 선택이라고 판단했다.

---

## 기술 스택 선택 이유

FastAPI는 키움 API 호출과 DB 작업이 섞인 비동기 I/O를 처리하려고 골랐다. PostgreSQL 16은 `docker-compose.yml`로 로컬 컨테이너를 띄우고 `psycopg[binary]`로 붙였다. 모델 학습·직렬화는 scikit-learn과 joblib을 썼고, `artifacts/baseline_model.joblib`로 저장한다. `server/modeling.py`는 scikit-learn이 없는 환경을 위해 정확도·정밀도·재현율·F1·ROC-AUC를 직접 계산하는 순수 Python fallback까지 갖췄다. 테스트는 pytest로, auth부터 backtest·benchmark·collector·storage까지 11개 파일에 나눠 관리한다.

---

## 벤치마크 설계 — 모델이 운이 좋았던 건 아닌지 확인

`server/benchmark.py`의 `BenchmarkEngine`은 모델 전략(top-k 선정)을 4가지 베이스라인과 비교한다. equal_weight(전종목 균등), buy_all(전부 매수), inverse_signal(모델 신호 반대로), 그리고 random_top_k(랜덤 top-k, seed=42로 100회 시행)다. 랜덤 100회 시행의 p95/p05 백분위수까지 계산해서, 모델 수익률이 랜덤 분포 대비 어느 위치에 있는지 판단한다. 모델이 단순히 운이 좋아서 수익이 난 건 아닌지를 구조적으로 검증하려는 의도다.

백테스트와 벤치마크는 `run_selected_records()`를 공유해서 현금·포지션·체결 규칙이 동일하다. 후보 선택 로직만 바꿔서 비교하는 구조라, 전략 차이 외의 변수가 섞이지 않는다. `BacktestConfig`에는 수수료 0.00015, 세금 0.0018, 슬리피지 0.0005를 반영했고 초기 자본은 1000만원으로 뒀다.

---

## 실패와 개선

커밋 로그에 "Potential fix for pull request finding"이라는 메시지가 반복됐다. 자동 코드 리뷰가 지적한 사항을 반영한 수정 커밋으로, PR#1~#3과 #5~#6에서 특히 많았다(PR당 2~9개).

명시적으로 남은 버그도 몇 개 있다. 모델 학습 검증 구간에서 미래 데이터가 새어 들어가는 validation horizon leakage를 발견해 수정했다. 시세 타임스탬프는 UTC로 저장되고 있었는데, 실제로는 한국 시간(KST) 기준이어야 해서 Asia/Seoul로 고쳤다. 백테스트 초기 구현에서는 현금과 미청산 포지션 회계가 어긋나는 버그가 있었다. 수집기에서는 `max_iterations`가 None일 때 결과 누적을 건너뛰는 버그와, `fail_fast=False`일 때 실패 결과가 기록에서 빠지는 버그를 각각 수정했다.

---

## 배운 점

플랫폼 제약(32bit COM)을 프로세스 경계로 바꾸면 각 프로세스는 자기 역할에만 집중할 수 있다. 다만 그 경계를 넘는 통신(websocket 명령/이벤트)의 실패 시나리오는 별도로 설계해야 한다는 걸 이번에는 충분히 다루지 못했다. 다음 단계는 32bit 노드가 끊겼을 때 64bit 서버가 어떻게 재연결하고 미완료 주문을 처리하는지를 명시적으로 테스트하는 것이다.

벤치마크를 랜덤 시행과 비교하는 구조를 처음부터 넣은 건 잘한 선택이었다. 백테스트 수익률 하나만 보고 모델을 판단했다면 랜덤보다 나은지조차 확인하지 못했을 것이다.

레포지토리는 [dorec9/seedagent](https://github.com/dorec9/seedagent)에 있다.
