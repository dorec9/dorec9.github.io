---
title: "이상치 탐지 실무 — Z-score·IQR부터 Isolation Forest까지, 방법 선택 기준"
date: 2026-07-29
categories: [data-statistics]
tags: [이상치탐지, Z-score, IQR, IsolationForest, LOF, DBSCAN, 데이터분석]
excerpt: "통계 기반과 머신러닝 기반 이상치 탐지 방법의 차이와 프로덕션 적용 기준을 정리한다"
---

유럽 지역 통계를 분석한 한 연구가 있다. 단변량 Z-score는 12개 지역을 이상치로 플래그했다. 같은 데이터에 다변량 Mahalanobis distance를 쓰자 3개 지역만 남았다([arXiv 2605.02884](https://arxiv.org/abs/2605.02884), 2026년 기준). 방법을 바꾸자 결과가 4배 차이 났다. 방법 선택에 따라 "이상치"의 정의 자체가 달라진다는 뜻이다. 이상치 탐지는 흔히 전처리 단계로 취급되지만, 방법을 잘못 고르면 결과 해석 전체가 흔들린다.

---

## 통계 기반 방법 — Z-score, IQR

Z-score는 데이터가 정규분포를 따른다고 가정하고, 평균에서 표준편차 절댓값 3을 넘는 값을 이상치로 분류한다. 계산이 단순하고 해석이 직관적이라 실무에서 가장 먼저 시도하는 방법이다.

IQR(사분위범위)은 분포 가정이 없는 비모수적 방법이다. Q1에서 1.5×IQR을 뺀 값보다 작거나, Q3에 1.5×IQR을 더한 값보다 크면 이상치로 본다. 분포가 한쪽으로 치우친(skewed) 데이터에서는 Z-score보다 IQR이 더 안정적이다([Let's Data Science 종합 가이드](https://letsdatascience.com/blog/finding-the-needle-a-comprehensive-guide-to-anomaly-detection-algorithms)).

문제는 두 방법 모두 단변량(변수 하나) 기준이라는 점이다. 변수 하나만 보면 정상 범위를 벗어난 것처럼 보이는 데이터가, 여러 변수를 함께 고려하면 정상 조합인 경우가 있다. 앞서 든 예시처럼 단변량 통계 방법은 과탐지(false positive) 경향이 있다.

---

## 머신러닝 기반 방법

### Isolation Forest

Isolation Forest는 무작위로 선택한 속성 기준으로 데이터를 반복 분할해 각 데이터 포인트를 격리한다([scikit-learn 이상치 탐지 가이드](https://scikit-learn.org/stable/modules/outlier_detection.html)). 정상 데이터는 격리까지 여러 번 분할이 필요하다. 이상치는 적은 분할 횟수로 격리된다. 거리나 밀도 계산 없이 트리 간 평균 경로 길이로 이상치 점수를 산출한다. 대규모·고차원 데이터에서도 튜닝 부담이 적은 이유다.

scikit-learn 공식 문서에 따르면 Isolation Forest의 `contamination` 파라미터는 데이터셋 내 이상치 비율을 나타내며 `'auto'` 또는 실수값을 받는다. 이 값에 따라 판정 임계값(offset)이 결정되므로, 예상 이상치 비율을 사전에 어림잡아 설정하는 것이 탐지 정확도에 직결된다([scikit-learn 공식 문서](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)).

### LOF, DBSCAN

LOF(Local Outlier Factor)는 이웃 데이터 대비 지역 밀도 편차를 측정해, 주변보다 밀도가 낮은 포인트를 이상치로 판단한다. DBSCAN은 밀도 기반 클러스터링 알고리즘으로, 어느 클러스터에도 속하지 않는 희소 영역의 데이터를 이상치로 라벨링한다([Analytics Vidhya의 IQR·Z-score·LOF·DBSCAN 비교](https://www.analyticsvidhya.com/blog/2022/10/outliers-detection-using-iqr-z-score-lof-and-dbscan/)).

LOF는 실시간성이 필요한 분야에서 실무 적용 사례가 있다. 금융권에서는 결제 처리 과정 중 자금이 실제로 빠져나가기 전 비정상 거래 패턴을 LOF로 탐지해 의심 거래를 차단하는 데 쓰인다([Number Analytics](https://www.numberanalytics.com/blog/practical-applications-of-outlier-detection-in-real-world-data-sets)).

---

## 방법 비교

| 방법 | 가정 | 강점 | 약점 |
|------|------|------|------|
| Z-score | 정규분포 | 계산 단순, 해석 쉬움 | 비대칭 분포에서 오탐 |
| IQR | 없음(비모수) | 치우친 분포에도 안정적 | 단변량, 다차원 관계 미반영 |
| Isolation Forest | 없음 | 고차원·대규모에 강함, 튜닝 최소 | contamination 설정에 민감 |
| LOF | 없음 | 지역 밀도 편차 포착, 실시간 적용 가능 | 이웃 수(k) 설정 필요 |
| DBSCAN | 없음 | 클러스터 형태 이상치 포착 | 밀도 파라미터 설정 까다로움 |

---

## 실무 적용 분야

Isolation Forest는 금융 사기 탐지, 네트워크 보안, 제조 공정의 결함 제품 탐지에 쓰인다([Isolation Forest 튜토리얼](https://www.datacamp.com/tutorial/isolation-forest)). 대량의 거래·로그 데이터를 낮은 연산 비용으로 판정할 수 있어서다. 국내 금융권도 룰 기반 이상거래탐지시스템(FDS)의 신종 사기 대응 한계를 극복하기 위해 AI·빅데이터 기반의 자가학습형 지능형 FDS로 전환하는 중이다([KCI 학술논문](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003320225)).

경찰청 통계에 따르면 2024년 국내 사이버사기 발생 건수는 100,539건으로 전년 대비 늘었다. 이 중 사이버투자 사기는 12,851건이다([경찰청 공공데이터포털](https://www.data.go.kr/data/15064572/fileData.do?recommendDataYn=Y), 2024년 기준). 룰 기반 탐지만으로는 늘어나는 신종 수법을 따라잡기 어렵다.

---

## 프로덕션 적용 기준

단일 알고리즘에 의존하면 오탐과 미탐 사이에서 트레이드오프를 피할 수 없다. 앞서 인용한 유럽 지역 통계 연구는 대안도 제시한다. 여러 탐지기를 결합해, 예를 들어 5개 방법 중 3개 이상이 동시에 플래그한 지점에만 사람의 검토를 집중시키는 앙상블 방식이다([arXiv 2605.02884](https://arxiv.org/abs/2605.02884)).

실무 파이프라인은 보통 단계를 나눈다. LOF 같은 거리 기반 방법으로 1차 필터링한 뒤 지도학습 분류기로 정제하는 구조가 하나다. 통계·거리 기반 방법으로 전처리한 뒤 오토인코더 같은 딥러닝 모델로 심화 분석하는 구조도 쓰인다([Number Analytics — 이상치 탐지 실무 적용 사례](https://www.numberanalytics.com/blog/practical-applications-of-outlier-detection-in-real-world-data-sets)).

이상치를 탐지한 다음 처리 방식도 정해둬야 한다. 명백한 입력 오류라면 제거하고, 결측치처럼 다뤄야 한다면 평균·중앙값으로 대체하고, 사기 거래처럼 중요한 신호라면 보존하고, 스케일 차이가 원인이라면 정규화로 해결한다([Let's Data Science 종합 가이드](https://letsdatascience.com/blog/finding-the-needle-a-comprehensive-guide-to-anomaly-detection-algorithms)).

---

## 방법 선택 체크리스트

1. 변수가 1개이고 정규분포에 가까운가 → Z-score
2. 변수가 1개이고 분포가 치우쳤는가 → IQR
3. 변수가 여러 개이고 데이터 규모가 큰가 → Isolation Forest
4. 실시간 판정이 필요하고 지역 밀도 차이가 중요한가 → LOF
5. 판정 결과가 중요한 의사결정(사기 차단, 품질 불량 등)으로 이어지는가 → 단일 방법 대신 앙상블 검토

---

## 정리

이상치 탐지에서 가장 먼저 확인할 점은 변수 개수와 분포 형태다. 단변량·정규분포면 Z-score, 치우친 분포면 IQR로 시작하면 된다. 변수가 여러 개이거나 데이터 규모가 크면 Isolation Forest나 LOF 같은 머신러닝 기반 방법이 필요하다. 판정 결과가 실제 의사결정으로 이어지는 상황이라면 단일 알고리즘 대신 여러 방법을 결합한 앙상블 검토가 오탐과 미탐을 동시에 줄이는 방법이다.
