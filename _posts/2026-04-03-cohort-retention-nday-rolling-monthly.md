---
title: "코호트 분석으로 리텐션 측정하기 — N-Day·Rolling·월간 리텐션의 차이와 선택 기준"
date: 2026-04-03
categories: [data-statistics]
tags: [코호트분석, 리텐션, N-Day리텐션, Rolling리텐션, 데이터분석, SaaS]
excerpt: "코호트 분석의 3가지 리텐션 지표(N-Day, Rolling, 월간)를 비교하고 서비스 유형별 선택 기준을 정리한다"
---

리텐션 지표를 처음 정리할 때 N-Day, Rolling, 월간 리텐션 중 무엇을 써야 할지 막혔다. 지표마다 같은 서비스를 놓고 다른 숫자가 나오기 때문이다. 어떤 지표를 선택하느냐에 따라 보고서의 결론이 달라지므로, 서비스 유형에 맞는 기준을 먼저 잡아야 한다.

---

## 코호트 분석이란

코호트(cohort)는 동일 시기에 특정 행동을 한 사용자 집단이다. 코호트 분석은 이 집단을 시간 축으로 추적해 이탈·복귀 패턴을 파악하는 기법이다([Amplitude](https://amplitude.com/explore/analytics/cohort-retention-analysis)).

코호트는 크게 3가지로 나뉜다.

1. **획득 코호트** — 가입일 기준으로 묶는다. 가장 많이 쓴다.
2. **행동 코호트** — 특정 기능을 처음 사용한 날 기준으로 묶는다.
3. **매출 코호트** — 첫 결제일 기준으로 묶는다.

핵심 원칙은 **달력 날짜가 아닌 Day 0(시작일) 기준 정렬**이다. 1월 1일에 가입한 사용자와 2월 1일에 가입한 사용자를 달력 날짜로 비교하면 경과 기간이 달라 코호트 간 비교 자체가 무의미해진다([Userpilot](https://userpilot.com/blog/cohort-analysis/)).

---

## 3가지 리텐션 지표

### N-Day 리텐션

코호트가 정확히 N일째 되는 날 활성 상태인 비율이다.

> 1,000명이 가입했고, 정확히 7일 뒤(D7)에 300명이 접속했다면 D7 리텐션은 30%다.

N일 당일에 접속하지 않으면 이탈로 간주한다. 따라서 일일 접속이 핵심인 게임·소셜미디어에 적합하다([Lenny's Newsletter](https://www.lennysnewsletter.com/p/measuring-cohort-retention)). 일간 활성 사용자(DAU)를 주 지표로 쓰는 서비스라면 D1, D7, D30 리텐션을 함께 추적하는 것이 일반적이다.

**단점**: 같은 사용자가 D6에 접속하고 D8에 접속해도 D7 리텐션에는 잡히지 않는다. 사용 빈도가 불규칙한 서비스에서는 이탈을 과대 계산한다.

---

### Rolling 리텐션 (Unbounded Retention)

N일 이후 특정 시점까지 **한 번이라도** 돌아온 비율이다. "언바운디드(Unbounded)" 리텐션이라고도 부른다([Count.co](https://count.co/metric/cohort-retention-analysis)).

> 1,000명 가입, D7 이후 30일 내에 한 번이라도 접속한 사람이 450명이라면 Rolling 30 리텐션은 45%다.

N-Day 리텐션보다 항상 같거나 높게 나온다. 이커머스처럼 사용자가 필요할 때만 접속하는 서비스에서 실제 이탈 여부를 더 정확히 반영한다([ThinkingData](https://www.thinkingdata.kr/blog/cohort-analysis-user-retention-strategy)).

**단점**: 분모가 시간이 지날수록 고정되지 않아, 장기 롤링 리텐션은 해석에 주의가 필요하다.

---

### 월간 리텐션 (MoM Retention)

전월 대비 당월 활성 사용자 비율이다. 공식은 아래와 같다.

```
월간 리텐션(%) = 전월 활성 사용자 중 당월에도 활성인 사용자 수 ÷ 전월 활성 사용자 수 × 100
```

B2B SaaS 구독 모델에서 주로 쓴다([뷰저블](https://www.beusable.net/blog/?p=4355)). 계약 단위가 월·연 단위이기 때문에 일간 접속 패턴보다 월간 유지 여부가 더 의미 있다.

업계 참고치: B2B SaaS의 평균 월간 리텐션은 약 95~97% 수준으로 알려져 있다([Lenny's Newsletter](https://www.lennysnewsletter.com/p/measuring-cohort-retention)). 월간 리텐션 95%는 연간 이탈률(churn)로 환산하면 약 46%에 해당하므로, 수치를 볼 때 연환산 이탈률도 함께 계산하는 것이 좋다.

---

## 서비스 유형별 선택 기준

| 서비스 유형 | 권장 지표 | 근거 |
|---|---|---|
| 게임 / 소셜미디어 | N-Day (D1, D7, D30) | 일일 접속이 핵심 지표 |
| 이커머스 / 유틸리티 앱 | Rolling | 비정기적 사용 패턴, 이탈 과대 계산 방지 |
| B2B SaaS 구독 | 월간 MoM | 계약 단위가 월·연간, 일간 변동 의미 없음 |

자료를 정리하면서 느낀 건, 지표 선택보다 일관성이 더 중요하다는 점이다. 같은 제품을 N-Day로 보다가 Rolling으로 바꾸면 수치가 올라간 것처럼 보인다. 하지만 실제 사용 행동은 변하지 않는다. 보고서에서 지표 정의를 한 번 정하면 바꾸지 않는 것이 원칙이다.

---

## 실무에서 자주 틀리는 3가지

### 1. 달력 날짜로 코호트를 자르는 실수

"1월에 가입한 사용자"처럼 달력 월 기준으로 잘라서 비교하면, 1월 1일 가입자(31일 추적 가능)와 1월 31일 가입자(1일 추적 가능)가 같은 코호트에 묶인다. Day 0 기준 정렬을 반드시 먼저 잡아야 한다([Amplitude](https://amplitude.com/explore/analytics/cohort-retention-analysis)).

### 2. 시즌 효과를 배제하지 않는 비교

이커머스라면 12월 코호트는 연말 특수로 초기 리텐션이 높게 잡힌다. 전월 대비 비교만 보면 계절성이 숨는다. 전년 동기 코호트와 YoY 비교를 병행해야 계절성을 분리할 수 있다([ThinkingData](https://www.thinkingdata.kr/blog/cohort-analysis-user-retention-strategy)).

### 3. 코호트 크기가 너무 작을 때 비율 해석

코호트 인원이 30명 미만이면 비율 변동 폭이 커서 신호인지 노이즈인지 구분하기 어렵다. 코호트별 n수를 리텐션 표 옆에 항상 표시하고, 표본이 작은 셀은 해석을 유보한다.

---

## 정리

이번 정리를 통해 확인한 점은, 지표 선택 전에 서비스의 핵심 사용 주기를 먼저 정의해야 한다는 것이다. 일간 접속이 가치를 만드는 서비스는 N-Day, 비정기 사용 패턴은 Rolling, 구독 계약 구조는 월간 MoM을 기본으로 잡는다.

다음 단계로는 코호트 리텐션 곡선이 평탄화(flatten)되는 구간을 찾아 **자연 리텐션율**을 파악하고, 그 시점까지 사용자를 이끄는 온보딩 흐름을 설계하는 작업으로 이어진다.

---

**참고 자료**
- [Amplitude — Cohort Retention Analysis](https://amplitude.com/explore/analytics/cohort-retention-analysis)
- [Userpilot — Cohort Analysis](https://userpilot.com/blog/cohort-analysis/)
- [Lenny's Newsletter — Measuring Cohort Retention](https://www.lennysnewsletter.com/p/measuring-cohort-retention)
- [ThinkingData — 코호트 분석 방법 총정리](https://www.thinkingdata.kr/blog/cohort-analysis-user-retention-strategy)
- [뷰저블 — 코호트 분석 이해하기](https://www.beusable.net/blog/?p=4355)
- [Count.co — Cohort Retention Analysis](https://count.co/metric/cohort-retention-analysis)
