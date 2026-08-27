---
title: "SQL 윈도우 함수로 지표 계산하기 — 누적합·전기대비·리텐션을 쿼리 한 번에 뽑는 5가지 패턴"
date: 2026-08-05
categories: [data-statistics]
tags: [SQL, 윈도우함수, ROW_NUMBER, LAG, 누적합, 리텐션쿼리, 지표계산, 데이터분석]
excerpt: "스프레드시트로 손계산하던 누적합·전월대비·리텐션을 SQL 쿼리 하나로 옮기는 패턴 5개를 정리한다"
---

월간 보고서를 만들 때 SQL로 원본만 뽑고 누적합과 전월대비 증감은 스프레드시트 수식으로 채웠다. 원본이 바뀌면 수식을 다시 끌어내려야 했고, 셀 범위가 어긋나 틀린 적도 있다. 이 계산을 쿼리로 옮기며 쓴 윈도우 함수 패턴 5개를 정리한다.

윈도우 함수(window function)는 현재 행뿐 아니라 여러 행에 걸쳐 값을 계산한다([PostgreSQL 공식 문서 — 윈도우 함수](https://www.postgresql.org/docs/current/tutorial-window.html)). `GROUP BY`와 달리 행을 합치지 않고 계산 열만 붙인다. MySQL 8.0.2([MySQL 공식 블로그](https://dev.mysql.com/blog-archive/mysql-8-0-2-introducing-window-functions/), 2017년 기준), SQLite 3.25.0([SQLite 공식 문서](https://sqlite.org/windowfunctions.html), 2018년 기준)에 들어갔다.

## 패턴 1. 사용자별 최신 1건만 남기기

`ROW_NUMBER()`는 파티션 안에서 1부터 순번을 매긴다([BigQuery 공식 문서 — Numbering functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions)). `PARTITION BY`는 행을 묶는 기준이다.

```sql
SELECT user_id, plan FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY user_id ORDER BY updated_at DESC) rn
  FROM subscriptions
) WHERE rn = 1;
```

## 패턴 2. 누적합 — 프레임을 직접 지정한다

```sql
SUM(revenue) OVER (ORDER BY order_date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) cum_revenue
```

`ROWS BETWEEN ...`을 빼면 값이 달라진다. 기본 프레임이 `RANGE UNBOUNDED PRECEDING`이라, 파티션 시작부터 **현재 행의 마지막 동순위(peer)까지** 포함한다([PostgreSQL 공식 문서 — 값 표현식](https://www.postgresql.org/docs/current/sql-expressions.html)). 원시 주문 로그에 쓰면 하루 안 모든 행에 같은 누적값이 찍힌다. 이걸 모르고 한 번 틀린 뒤로 `ROWS`를 명시한다.

## 패턴 3. 전기대비 증감 — LAG

`LAG()`는 같은 파티션에서 지정한 칸수만큼 앞선 행 값을 가져온다([BigQuery 공식 문서 — Navigation functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions)).

```sql
ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
  * 100.0 / LAG(revenue) OVER (ORDER BY month), 1) mom_pct
```

전년동월대비는 `LAG(revenue, 12)`다. 함정은 결측 월이다. 4월이 비면 `LAG(1)`은 3월이 아니라 그 앞 행을 집는다. 날짜가 아니라 행 기준이다. 월 축을 먼저 만들어 빈 달을 채워야 한다.

## 패턴 4. 리텐션 — 코호트 기준일을 행마다 붙인다

첫 활동일을 붙이고, 간격을 구하고, 간격별로 집계한다. 첫 단계에 자기조인 대신 `MIN() OVER`를 쓴다.

```sql
WITH base AS (
  SELECT user_id, activity_date,
    MIN(activity_date) OVER (PARTITION BY user_id) cohort_date
  FROM activities )
SELECT cohort_date,
  DATE_DIFF(activity_date, cohort_date, DAY) day_n,
  COUNT(DISTINCT user_id) users
FROM base GROUP BY 1, 2;
```

`COUNT(DISTINCT user_id)`가 중요하다. 리텐션은 사용자 단위 지표라 같은 날 여러 번 접속해도 1명이다.

## 패턴 5. 전체 대비 구성비

`OVER ()`를 비워두면 파티션이 전체 1개가 된다. `ROUND(revenue * 100.0 / SUM(revenue) OVER (), 1)`로 끝난다. 합계를 따로 구해 조인할 일이 없다.

## 자주 막히는 지점 — WHERE에 못 쓴다

윈도우 함수는 `SELECT` 목록과 `ORDER BY`에서만 쓸 수 있다(위 PostgreSQL 문서). `WHERE`가 먼저 실행되기 때문이다. 그래서 패턴 1처럼 서브쿼리로 감싸 걸러야 한다.

Snowflake와 BigQuery에는 `QUALIFY`가 있다. `HAVING`이 `GROUP BY`에 하는 일을 윈도우 함수에 하는 절이다([Snowflake 공식 문서 — QUALIFY](https://docs.snowflake.com/en/sql-reference/constructs/qualify)). 결과는 같은데 중첩이 사라진다. PostgreSQL에는 없다.

```sql
SELECT user_id, plan FROM subscriptions
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id
  ORDER BY updated_at DESC) = 1;
```

## 정리

다섯 패턴 모두 `OVER (PARTITION BY ... ORDER BY ... 프레임)` 세 칸을 무엇으로 채울지 정하는 문제였다. 함수를 새로 외울 일이 아니다. 다음 단계는 성능이다. 윈도우 함수는 파티션 단위 정렬을 동반한다. 대시보드용 쿼리는 파티션 키에 인덱스를 건 뒤 실행계획을 확인할 생각이다.
