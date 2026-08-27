---
title: "이탈을 시점으로 모델링하기 — Kaplan-Meier 곡선과 Cox 비례위험 적용 기준"
date: 2026-08-12
categories: [data-statistics]
tags: [생존분석, KaplanMeier, Cox비례위험, 이탈예측, censoring, lifelines]
excerpt: "코호트 표는 몇 %가 남았는지만 센다. 생존 분석은 언제 떠나는지와 무엇이 위험을 키우는지를 답한다"
---

리텐션 코호트 표를 몇 달 돌리다 막혔다. "3개월 차 잔존율"까지는 표로 나온다. 그런데 "언제 떠나는가"와 "어떤 고객이 더 빨리 떠나는가"는 안 나온다. 생존 분석(survival analysis, 사건까지 걸린 시간을 다루는 통계 기법)을 실무에 붙일 때의 판단 기준을 정리한다.

---

## 집계 관점이 못 푸는 두 가지

첫째, 아직 안 떠난 고객이다. 관측 종료 시점까지 남아 있는 고객은 이탈 시점을 모른다. 이걸 우측 절단(right censoring)이라 한다. 코호트 표는 이들을 생존으로 세고 끝낸다.

둘째, 요인별 순효과다. 계약 유형과 부가서비스가 각각 이탈 위험을 얼마나 올리는지, 다른 조건을 통제한 값은 표로 안 나온다.

---

## 절단을 잘못 다루면 추정이 한쪽으로 틀어진다

흔한 실수는 절단된 관측치를 이탈 시점처럼 쓰는 것이다. 가입 90일 된 활성 고객은 "90일 생존"이 아니라 "최소 90일 이상"이다.

절단된 고객을 빼고 계산하면 생존 확률이 낮게 추정된다([scikit-survival 공식 문서 — 생존 분석 입문](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)). 반대 방향 편향도 있다. 임상 데이터에서는 추적 손실형 절단이 Kaplan-Meier 생존을 과대추정하는 쪽으로 밀었다([우측 절단 편향 연구 — arXiv](https://arxiv.org/abs/2012.08649), 2020년 기준). 어느 쪽이든 절단 처리를 건너뛰면 이탈률은 틀린다.

---

## Kaplan-Meier — 이탈 시점의 분포를 본다

Kaplan-Meier 추정량은 절단 데이터를 버리지 않고 생존 곡선을 그린다. 각 시점에서 위험집합(그때까지 남아 있던 고객 수)을 다시 세므로, 절단된 고객도 그 시점까지는 분모에 들어간다.

세그먼트별 곡선을 겹치고 로그순위 검정(log-rank test)으로 차이가 유의한지 본다. IBM Telco 공개 데이터에서는 계약 유형, 부가서비스, 인구통계 변수의 생존 분포 차이가 유의했다([IBM Telco 생존 분석 — Atlantis Press ICATAM 2024](https://www.atlantis-press.com/proceedings/icatam-24/126004727), 2024년 기준).

---

## Cox 비례위험 — 위험비로 요인을 읽는다

Cox 비례위험 모형은 각 변수의 계수를 지수변환해 위험비(hazard ratio, HR)로 읽는다. HR 0.6이면 이탈 위험이 기준 대비 40% 낮다는 뜻이다.

같은 Telco 데이터를 Cox로 돌린 사례에서는 다년 계약 고객이 월 단위 계약보다 덜 해지했고, 72개월 뒤에도 60% 이상이 남았다([Telco 이탈 생존 분석 사례 — Zach Angell](https://medium.com/@zachary.james.angell/applying-survival-analysis-to-customer-churn-40b5a809b05a), 2019년 기준).

성능은 일치도 지수(C-index, 생존 분석에서 AUC에 대응하는 지표로 0.5가 무작위)로 본다. 계약형 유틸리티 서비스 연구에서 Cox의 C-index는 6개월 상품 72%, 12개월 상품 79%였다([Journal of Marketing Analytics](https://link.springer.com/article/10.1057/s41270-025-00450-2), 2025년 기준). 같은 연구의 Aalen 가법 모형은 계약 만료 전 구간에서 58~61%에 그쳤다.

Python은 lifelines의 `KaplanMeierFitter`, `CoxPHFitter`로 붙인다. 기간 열과 사건 열을 분리해 넣는다([lifelines 논문 — JOSS](https://joss.theoj.org/papers/10.21105/joss.01317), 2019년 기준).

---

## 비례위험 가정을 검정하지 않으면 해석이 틀린다

"비례"는 변수 효과가 시간에 따라 일정하다는 가정이다. 가입 1개월 차와 24개월 차에서 계약 유형의 효과가 같아야 한다. 관측 기간 내내 이 가정이 성립하는지 확인하는 일이 Cox 모형에서 가장 중요한 절차로 꼽힌다([Survival analysis part II — KJA](https://pmc.ncbi.nlm.nih.gov/articles/PMC6781220/), 2019년 기준). 가정이 깨진 상태에서 뽑은 HR은 전체 기간 평균으로 뭉개진 값이라 시점별 의사결정에 못 쓴다.

검정은 Schoenfeld 잔차로 한다. 추정값과 관측값의 차이가 시간과 상관을 갖는지 본다. lifelines에서는 `CoxPHFitter.check_assumptions()`가 위반 변수를 출력한다([lifelines 문서](https://lifelines.readthedocs.io/en/latest/fitters/regression/CoxPHFitter.html)).

위반이 나오면 해당 변수를 층으로 빼는 층화 Cox나 시간 의존 Cox로 대응한다. 같은 해설 논문이 든 표준 대응이다.

---

## 실무 적용 순서

1. 가입일·관측 종료일·이탈 여부 세 열로 기간과 사건을 분리한다
2. 절단 비율을 센다 — 절반이 넘으면 단순 이탈률 보고를 멈춘다
3. Kaplan-Meier로 곡선을 그려 이탈이 몰리는 구간을 찾는다
4. 세그먼트별 곡선을 겹쳐 로그순위 검정으로 차이를 본다
5. Cox로 HR을 뽑는다 — C-index 0.7 미만이면 변수 설계를 다시 본다
6. Schoenfeld 잔차로 가정을 검정하고, 위반 변수는 층으로 뺀다

---

## 정리

코호트 표와 생존 분석은 대체재가 아니다. 표는 몇 % 남았나를 공유할 때 쓰고, 생존 분석은 언제 왜 떠나는가를 판단할 때 쓴다. 갈리는 지점은 절단 비율과 비례위험 가정 검정이다. 둘을 건너뛰면 숫자는 나오지만 해석이 틀린다. 다음은 같은 데이터에서 Cox와 랜덤 생존 포레스트의 C-index를 비교할 차례다.
