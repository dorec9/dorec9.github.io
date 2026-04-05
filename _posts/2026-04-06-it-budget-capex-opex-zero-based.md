---
title: "IT 예산 수립 실무 — CAPEX·OPEX 구분과 제로베이스 예산 편성법"
date: 2026-04-06
categories: planning-insight
tags: [IT예산, CAPEX, OPEX, 제로베이스예산, 예산편성, IT기획]
excerpt: "IT 예산에서 CAPEX와 OPEX를 구분하는 기준과 제로베이스 예산 편성의 실무 적용법을 정리한다"
---

IT 예산 편성 시즌마다 반복되는 질문이 있다. "이 항목은 CAPEX야, OPEX야?" 분류 기준이 흔들리면 CFO 보고서와 세무 처리가 엇갈린다. 이 글에서는 CAPEX·OPEX 구분 기준과 제로베이스 예산(ZBB) 적용 순서를 정리한다.

---

## IT 예산의 구조: Run·Grow·Transform

Gartner는 2026년 전 세계 IT 지출이 $6.15조(약 8,400조 원)에 달할 것으로 전망한다.[^gartner] 이 규모에도 불구하고 기업 내부에서 예산 싸움은 매번 반복된다. 이유는 단순하다. 대부분의 예산이 현행 유지에 묶이기 때문이다.

업계 조사에 따르면 기업 IT 예산의 55~72%는 현행 운영 유지(Run)에 소비된다.[^rgt] 혁신이나 성장에 쓸 수 있는 비율(Grow/Transform)은 19~28%에 그친다. 예산 편성의 첫 번째 작업은 지금 어디에 돈이 쏠리고 있는지 확인하는 것이다.

- **Run**: 기존 시스템 유지, 라이선스 갱신, 보안 패치
- **Grow**: 기능 추가, 디지털 채널 확장, 데이터 분석 고도화
- **Transform**: 레거시 전환, 플랫폼 재구축, 신규 사업 기반 구축

---

## CAPEX vs OPEX: 분류 기준

**CAPEX(Capital Expenditure, 자본적 지출)**는 장기 자산에 대한 일시적 투자다. 서버 구매, 네트워크 장비, 영구 라이선스가 여기 해당한다. 감가상각(Depreciation)을 통해 비용이 수년에 걸쳐 분산된다.

**OPEX(Operating Expenditure, 운영비)**는 일상 운영에 드는 반복 비용이다. 클라우드 구독료, SaaS 라이선스, 유지보수 계약이 대표적이다. 발생한 회계 연도에 즉시 비용으로 처리된다.[^splunk]

실무에서 판단이 흔들리는 경우는 대부분 클라우드 전환 항목이다. 온프레미스 서버 $100,000 구매는 CAPEX다. 같은 용량의 클라우드를 월 $2,500에 임차하면 OPEX다.[^toolkitcafe] 하드웨어를 사느냐, 사용권을 빌리느냐로 구분하면 된다.

| 항목 | 분류 | 처리 방식 |
|---|---|---|
| 서버·네트워크 장비 구매 | CAPEX | 감가상각 (5~7년) |
| 데이터센터 구축 | CAPEX | 감가상각 |
| 영구 소프트웨어 라이선스 | CAPEX | 감가상각 또는 즉시 비용 |
| AWS·Azure·GCP 사용료 | OPEX | 당해 연도 즉시 비용 |
| SaaS 구독 (M365, Salesforce 등) | OPEX | 당해 연도 즉시 비용 |
| 유지보수·기술지원 계약 | OPEX | 당해 연도 즉시 비용 |

---

## 클라우드 전환이 CAPEX를 OPEX로 옮기고 있다

Gartner 2026년 전망에서 소프트웨어 지출은 전년 대비 +14.7%, 클라우드 인프라(데이터센터)는 +31.7% 성장이 예측된다.[^gartner] 이 두 항목은 거의 전부 OPEX다.

CFO 입장에서 OPEX 선호에는 3가지 이유가 있다.[^toolkitcafe]

1. **현금 유동성 확보**: 대규모 선투자 없이 월 단위 지출로 분산된다.
2. **유연한 확장·축소**: 수요 변동에 따라 지출을 조정할 수 있다.
3. **좌초 자산 제거**: 5~7년 하드웨어 수명주기에서 벗어날 수 있다.

반면 OPEX 전환의 위험도 있다. 사용량 관리가 느슨하면 총소유비용(TCO)이 CAPEX보다 높아진다. 클라우드 비용 최적화(FinOps)가 별도 관리 영역으로 떠오른 이유다.

---

## 제로베이스 예산(ZBB): 언제, 어떻게 쓰는가

**제로베이스 예산(Zero-Based Budgeting, ZBB)**은 매 예산 주기마다 모든 항목을 백지에서 재정당화하는 방식이다. 전년도 예산에 일정 비율을 더하는 증분 방식(Incremental Budgeting)과 정반대다.

ZBB를 적용한 기업은 비필수 영역에서 평균 10~25%의 운영비를 절감했다는 조사 결과가 있다.[^zbb] IT 예산에서도 오래된 구독 서비스, 중복 라이선스, 사용률이 낮은 인프라를 걸러내는 데 쓸 수 있다.

단점도 명확하다. 모든 항목을 매년 재정당화하려면 거버넌스 오버헤드가 크다. 중소 규모 IT팀이 전체를 ZBB로 운영하기는 현실적으로 어렵다.

실무에서는 **하이브리드 방식**이 현실적이다. Run 영역(서버 유지, 필수 라이선스)은 증분 방식으로 관리하고, Grow/Transform 항목은 ZBB로 재정당화한다.[^zbbhybrid] 새로운 투자 요청이 들어올 때마다 "왜 필요한가"를 묻는 구조를 만드는 것이다.

---

## 실무 적용 순서: 5단계

**1단계 — 지출 분류**
전년도 지출 내역을 CAPEX/OPEX, 그리고 Run/Grow/Transform으로 분류한다. ERP 데이터와 구매 대장을 함께 참조해야 한다.

**2단계 — Run 비율 점검**
Run 비율이 70%를 넘으면 최적화 대상을 식별한다. 사용률이 낮은 인프라와 중복 SaaS 구독이 첫 검토 대상이다.

**3단계 — Grow/Transform 항목 재정당화**
신규 또는 증액 요청 항목에 ZBB를 적용한다. 요청자가 "기대 효과(KPI), 측정 방법, 검증 기간"을 함께 제시하도록 템플릿화한다.

**4단계 — CAPEX → OPEX 전환 검토**
온프레미스 갱신 시점이 된 장비를 클라우드로 전환하면 당해 CAPEX 지출을 줄일 수 있다. 단, 3년 TCO를 비교해 OPEX 누적이 더 크지 않은지 확인한다.

**5단계 — 분기별 편차 점검**
예산 편성은 연간 작업이지만, 집행 편차는 분기 단위로 점검한다. 클라우드 비용은 분기 내에도 계획 대비 초과가 누적되기 쉽다.

---

## 정리

CAPEX와 OPEX 구분은 재무 처리의 문제이기도 하지만, 예산 유연성과 현금흐름 전략의 문제다. 클라우드가 확대될수록 IT 예산의 무게 중심은 OPEX 쪽으로 계속 이동한다. ZBB는 모든 항목에 적용하기보다 신규 투자 영역에 집중적으로 쓸 때 실용적이다.

다음 단계는 IT 예산 요청서(Business Case) 작성과 경영진 보고 형식이다. CAPEX·OPEX 구분과 ZBB 논리를 실제 보고 문서로 연결하는 방법을 다룬다.

---

[^gartner]: Gartner, "Gartner Forecasts Worldwide IT Spending to Grow 10.8% in 2026, Totaling $6.15 Trillion" (2026.02.03). 소프트웨어 +14.7%, 데이터센터 +31.7% 성장 전망 포함. [원문](https://www.gartner.com/en/newsroom/press-releases/2026-02-03-gartner-forecasts-worldwide-it-spending-to-grow-10-point-8-percent-in-2026-totaling-6-point-15-trillion-dollars)
[^rgt]: Awecomm, "IT Budgeting: Rethinking the Run, Grow, Transform Model - 2026 Update". 기업 IT 예산의 55~72%가 Run에 소비되며 Grow/Transform 비율은 19~28%. [원문](https://awecomm.com/Blog/it-budgeting-rethinking-the-run-grow-transform-model-2026-update/)
[^splunk]: Splunk, "CapEx vs. OpEx: Key Definitions and Differences". CAPEX는 감가상각, OPEX는 당해 연도 즉시 비용 처리. [원문](https://www.splunk.com/en_us/blog/learn/capex-vs-opex.html)
[^toolkitcafe]: ToolkitCafe, "CapEx vs OpEx: Complete Guide". 서버 구매 $100K 대 클라우드 월 $2,500 비교 사례. CFO 관점 3가지 이점 포함. [원문](https://toolkitcafe.com/blog/capex-vs-opex-complete-guide)
[^zbb]: Prophix, "Zero-based budgeting: pros and cons" (2025). ZBB 도입 기업의 비필수 영역 10~25% 절감 조사 결과. [원문](https://www.prophix.com/blog/zero-based-budgeting-pros-and-cons/)
[^zbbhybrid]: IBM, "What is zero-based budgeting?" 하이브리드 ZBB: 예측 가능한 반복 비용은 증분 방식, 재량 지출·프로젝트 기반 항목은 ZBB 적용. [원문](https://www.ibm.com/think/topics/zero-based-budgeting)
