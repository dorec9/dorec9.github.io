---
title: "TAM·SAM·SOM으로 시장 규모 추정하기 — Top-down과 Bottom-up 결합법"
date: 2026-04-05
categories: [business-economy]
tags: [TAM, SAM, SOM, 시장규모, 사업계획서, IR, 경영분석]
excerpt: "사업계획서에서 쓰이는 TAM/SAM/SOM 개념과 Top-down·Bottom-up 방식을 결합해 시장 규모를 추정하는 실무 방법을 정리한다"
---

시장 규모 슬라이드는 IR 덱에서 가장 자주 지적받는 페이지다. VC 가이드를 비교해 읽다 보면 공통된 판단 기준이 보인다. 숫자 크기보다 계산 근거가 핵심이다. 이 글에서는 TAM·SAM·SOM 구조와 Top-down·Bottom-up 방식을 결합해 시장 규모를 추정하는 방법을 정리한다.

---

## TAM·SAM·SOM이란

세 개념은 시장을 동심원처럼 좁혀가는 구조다.

**TAM(Total Addressable Market, 전체 시장)**  
제품 또는 서비스가 시장 전체를 점유했을 때 얻을 수 있는 총 수익 규모다. 경쟁자나 지역 제약 없이 이론상 최대치를 나타낸다.

**SAM(Serviceable Available Market, 유효 시장)**  
TAM 중에서 자사가 실제로 접근 가능한 영역이다. 지리적 범위, 유통 채널, 언어, 규제 등을 반영해 좁힌다. Antler의 계산 가이드에 따르면 SAM은 잠재 고객 수 × 고객당 연간 수익(ACV)으로 산출한다.

**SOM(Serviceable Obtainable Market, 수익 시장)**  
SAM 중 현실적으로 확보 가능한 점유율이다. 보통 첫 3~5년 매출 목표와 연결된다. Seedblink(2025)는 SOM을 "보유 자원, 경쟁 강도, 실행 역량을 반영한 수치"로 정의한다.

---

## 두 가지 추정 방식

### Top-down (하향식)

공신력 있는 산업 통계에서 출발해 우리 제품군으로 좁혀 내려오는 방식이다.

**흐름 예시 (밀키트)**  
국내 온라인 식품 시장 30조 원 → 밀키트 하위 카테고리 3조 원 → 프리미엄 밀키트 6,000억 원

- 장점: 통계청·산업 보고서 등 공인 데이터를 쓰므로 상한선에 신뢰도가 높다
- 단점: 우리 제품에 딱 맞는 데이터가 없으면 추정치가 뭉뚱그려진다. 투자자는 이를 "게으른 접근"으로 읽는다 ([Antler, 2024](https://www.antler.co/blog/tam-sam-som))

### Bottom-up (상향식)

단위 매출 요소를 곱해 쌓아 올리는 방식이다.

**기본 공식**  
```
시장 규모 = 잠재 고객 수 × 고객당 연간 구매액(ACV)
```

**B2B SaaS 예시**  
국내 대기업 1만 개 × 연 ACV 1,200만 원 = SAM 1,200억 원

**의료 소프트웨어 예시** ([Antler, 2024](https://www.antler.co/blog/tam-sam-som))  
호주 병원 1,352개 × 연 라이선스 1,000달러 → TAM 135만 달러  
공립 병원 695개만 대상 → SAM 69.5만 달러

- 장점: 실제 가격 구조와 고객 정의가 반영돼 투자자가 더 신뢰한다
- 단점: 잠재 고객 수와 ACV 가정을 검증하는 데 시간이 걸린다

---

## 결합 전략: 상한과 하한을 함께 제시한다

[Qubit Capital 상향식 시장 규모 추정 가이드](https://qubit.capital/blog/bottom-up-market-sizing)는 두 방식을 병행해 범위를 제시하는 구조를 권장한다. 실무 적용 방법은 다음과 같다.

1. Top-down으로 TAM 상한선을 설정한다 (Gartner·IDC·통계청 등 인용)
2. Bottom-up으로 SAM·SOM 하한선을 계산한다 (고객 수 × ACV)
3. 두 방식 추정치 차이가 3~5배 이상이면 가정 중 오류가 있다는 신호다
4. 슬라이드에는 두 방식을 모두 표기해 "큰 그림과 현실성"을 함께 보여준다

[ForumVC의 시장 규모 정의 가이드](https://www.forumvc.com/thought-pieces/understand-and-define-your-market-size)는 투자자들이 TAM보다 SAM·SOM에 더 주목한다고 분석한다. TAM이 수조 원이어도 SOM이 구체적이지 않으면 미팅이 끊기는 경우가 많다.

---

## 사업계획서·IR 적용 시 확인할 3가지

### SOM과 3년 매출 목표의 정합성

SOM이 100억 원으로 추정되면 3년차 매출 목표는 그 범위 안에 있어야 한다. SOM 100억에 3년차 목표 500억을 설정하면 논리 구조가 무너진다. SOM은 투자자가 매출 계획 현실성을 검증하는 기준점이다.

### 투명한 근거 제시 효과

투자자들이 공통적으로 지적하는 포인트는 "계산 근거"다. [Seedblink의 피칭 가이드(2025)](https://seedblink.com/blog/2025-02-25-pitch-perfect-how-to-present-tam-sam-som-to-win-over-your-investors)는 TAM 숫자 자체보다 어떻게 산출했는지를 슬라이드에 명시하라고 권고한다. 근거 없는 큰 숫자는 신뢰를 떨어뜨린다.

### 하나만 쓰면 생기는 문제

- Top-down만: "숫자는 크지만 너와 무관하다"는 반응이 나온다
- Bottom-up만: "시장이 너무 좁다"는 반응이 나온다
- 둘 다: 큰 기회 + 실행 가능성을 동시에 보여준다

---

## 흔한 오류 3가지

**TAM을 전 세계로 잡기**  
접근 불가능한 지역까지 포함하면 SAM을 좁히는 의미가 사라진다. TAM은 현실적인 최대 범위로 잡아야 SAM 비율이 설득력을 갖는다.

**SOM 산정 근거 없음**  
"시장 점유율 5% 목표"를 근거 없이 선언하는 경우가 많다. 경쟁사 점유율, 영업 파이프라인, 파트너 채널 수 등 구체적 가정이 필요하다.

**CAGR 단순 연장 적용**  
CAGR(연평균성장률)을 5~10년 후까지 같은 비율로 연장하면 과대 추정이 된다. 시장 성숙도와 포화 시점을 함께 제시해야 한다.

---

## 마무리: 다음에 확인할 것

자료를 정리하면서 확인한 점은, 계산 자체보다 "SOM이 3년 재무 모델과 연결되어 있는가"가 더 중요하다는 것이다. 숫자를 산출한 뒤 매출 계획, 마케팅 예산, 채용 계획과 정합성을 점검해야 한다.

다음 단계는 경쟁 분석(시장 지도)이다. GTM(Go-to-Market) 전략과 연결해 SOM 달성 경로를 구체화한다.

---

**참고 자료**
- [Antler — TAM, SAM & SOM: How To Calculate The Size Of Your Market](https://www.antler.co/blog/tam-sam-som)
- [Seedblink — Pitch Perfect: How to Present TAM, SAM & SOM to Win Over Your Investors (2025)](https://seedblink.com/blog/2025-02-25-pitch-perfect-how-to-present-tam-sam-som-to-win-over-your-investors)
- [ForumVC — Market Sizing for Startups: TAM, SAM, SOM Explained](https://www.forumvc.com/thought-pieces/understand-and-define-your-market-size)
- [Qubit Capital — Bottom-up Market Sizing](https://qubit.capital/blog/bottom-up-market-sizing)
- [Amazon Advertising — TAM, SAM, SOM 가이드](https://advertising.amazon.com/ko-kr/library/guides/tam-sam-som)
