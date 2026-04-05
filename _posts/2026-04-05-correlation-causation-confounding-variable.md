---
title: "상관관계를 인과관계로 착각하는 순간 — 교란변수와 3가지 검증 조건"
date: 2026-04-05
categories: data-statistics
tags: [상관관계, 인과관계, 교란변수, 통계분석, 데이터분석, 인과추론]
excerpt: "상관관계와 인과관계 혼동이 생기는 구조를 교란변수·역인과·데이터 과적합 사례로 정리한다"
---

데이터를 보다 보면 두 수치가 같이 오르내리는 걸 발견하고 "이게 원인이구나"라고 결론 내리고 싶어진다. 그 충동이 얼마나 자주 틀리는지 사례를 정리하면 생각보다 많다. 이 글은 혼동이 생기는 3가지 구조와 인과관계를 검증하는 3가지 조건을 정리한다.

---

## 1. 두 개념의 차이

**상관관계(Correlation)**는 두 변수가 함께 움직이는 통계적 연관성이다. 한 변수가 오를 때 다른 변수도 오르거나 내린다는 패턴만 말한다.

**인과관계(Causation)**는 한 변수의 변화가 다른 변수의 변화를 직접 일으키는 관계다. 방향성과 메커니즘이 있어야 한다.

"상관관계는 인과관계가 아니다(Correlation does not imply causation)"는 통계 분석에서 가장 자주 인용되는 경고다 ([DataCamp — Correlation vs. Causation](https://www.datacamp.com/blog/data-demystified-correlation-vs-causation)).

---

## 2. 혼동이 생기는 3가지 구조

### A. 교란변수(Confounding Variable) — 제3의 변수

교란변수란 두 변수 모두에 영향을 주어 상관처럼 보이게 만드는 외부 요인이다.

자료를 보면 고전적 사례들이 반복된다.

- 아이스크림 판매량이 늘면 익사 사망자도 늘어난다. 둘 다 "여름 기온"이 올리는 것이다.
- 어린이 신발 크기와 읽기 실력은 양의 상관이 있다. 공통 원인은 "나이"다.
- 운동량과 피부암 발생률이 함께 오르는 경우가 있다. "햇빛 노출 시간"이 교란변수다.

교란변수를 보지 않으면 원인 없는 정책을 내리게 된다 ([Statology — Correlation, Causation and Confounding](https://www.statology.org/correlation-causation-confounding-decoding-hidden-relationships-data/)).

### B. 역인과관계(Reverse Causality) — 방향 문제

두 변수 사이에 실제 관계가 있더라도 방향을 반대로 읽으면 틀린다.

비타민 D 수치가 낮으면 우울증 위험이 높다는 상관은 반복 관찰된다. 그런데 비타민 D 부족이 우울증을 유발하는 것인지, 우울증 상태(실내 생활, 일조량 감소)가 비타민 D를 낮추는 것인지 방향이 불명확하다.

eBay 사례가 더 직접적이다. Blake, Nosko, Tadelis(2015)가 Econometrica에 발표한 대규모 현장 실험에서 eBay 브랜드 키워드 검색광고의 매출 기여는 거의 없는 것으로 나타났다. 광고를 통해 유입된 트래픽의 99.5%는 광고 없이도 사이트에 접속했을 사용자였다. 검색광고가 구매를 만든 게 아니라, 이미 구매 의사가 있던 사용자가 광고를 클릭한 것이다 ([NBER Working Paper 20171 — Consumer Heterogeneity and Paid Search Effectiveness](https://www.nber.org/papers/w20171)).

### C. 데이터 드레징(Data Dredging) — 우연한 상관

충분히 큰 데이터셋에서 무관한 변수를 많이 검색하면 통계적으로 유의한 상관이 우연히 나온다. 유의 수준 5%를 기준으로 삼으면 100개 변수 조합 중 평균 5개는 무작위로 유의하게 나온다.

Tyler Vigen의 Spurious Correlations 프로젝트는 이 현상을 시각적으로 정리한 학술 프로젝트다. 니콜라스 케이지 출연 영화 수와 수영장 익사 사망자 수가 연도별로 강한 양의 상관을 보인다 ([Tyler Vigen — Spurious Correlations](https://www.tylervigen.com/spurious-correlations)). 인과 메커니즘이 없는 상관이다.

---

## 3. 인과관계 검증 3가지 조건

데이터에서 인과관계를 주장하려면 3가지를 모두 충족해야 한다 ([DataCamp — Correlation vs. Causation](https://www.datacamp.com/blog/data-demystified-correlation-vs-causation)).

1. **시간적 선후(Temporal Precedence)**: 원인이 결과보다 시간상 앞서 발생해야 한다. 광고 집행이 구매보다 먼저 일어났는지 확인한다.

2. **공변성(Covariation)**: 원인과 결과 사이에 통계적 상관이 존재해야 한다. 원인이 바뀔 때 결과도 변하는지 측정한다.

3. **외부 요인 배제(Elimination of Alternatives)**: 제3의 변수가 두 변수 모두를 설명하지 않음을 확인해야 한다. 교란변수를 분석에 포함하거나 실험적으로 통제한다.

3가지 중 하나라도 빠지면 인과 주장은 취약하다.

---

## 4. 실무 검증 방법 4가지

### 무작위 대조 실험(RCT)

교란변수를 두 집단에 균등하게 배분하는 가장 확실한 방법이다. A/B 테스트가 이 범주에 속한다. 처치군과 대조군을 무작위 배정하면 교란변수의 영향이 상쇄된다 ([Statology — Correlation, Causation and Confounding](https://www.statology.org/correlation-causation-confounding-decoding-hidden-relationships-data/)).

### 통계적 통제

실험이 어려울 때 회귀분석에서 교란변수를 독립변수로 포함한다. 예를 들어 "광고 노출"이 매출에 미치는 영향을 분석할 때 "기존 고객 여부"를 통제변수로 넣으면 교란 효과를 수치로 분리할 수 있다.

### 자연 실험(Natural Experiment)

정책 변화, 지역 차이, 자연재해처럼 연구자가 개입하지 않은 준실험 상황을 활용한다. 처치가 임의로 발생한 상황이어서 교란변수 통제가 가능하다.

### 가설 먼저 검증

상관을 발견하면 분석 전에 "이 관계를 설명할 수 있는 제3의 변수는 무엇인가"를 먼저 쓴다. 후보 교란변수 목록을 만든 뒤 데이터에서 통제한다. 상관을 확인한 뒤 해석을 짜 맞추면 편향이 생긴다.

---

## 5. 경영 실무 적용 시 체크리스트

자료를 보면 반복되는 실수 패턴이 있다.

- 만족도와 매출의 상관을 발견하면 "만족도를 높이면 매출이 오른다"고 결론 내린다. 그런데 제품 품질이 만족도와 매출 모두를 만드는 교란변수일 수 있다.
- 마케팅 채널별 전환율을 비교할 때 기존 고객 비율이 채널마다 다르면 교란이 생긴다.
- 시계열 데이터에서 두 지표가 같이 오르면 경기 사이클이나 계절성이 공통 원인일 수 있다.

상관을 발견했을 때 인과로 넘어가는 속도를 늦추는 것이 핵심이다.

---

## 결론

두 수치가 같이 움직인다는 관찰은 분석의 시작이지 결론이 아니다. 교란변수·역인과·우연한 상관 3가지 구조 중 어디에 해당하는지를 따지는 것이 분석자의 일이다. 인과 주장을 할 때는 시간적 선후, 공변성, 외부 요인 배제 3가지를 모두 충족했는지 체크하는 것이 최소한의 기준이다.

다음 단계로는 성향 점수 매칭(Propensity Score Matching)과 이중차분법(Difference-in-Differences) 같은 인과추론 기법을 통해 실험이 불가능한 상황에서 인과 효과를 추정하는 방법을 다룰 예정이다.
