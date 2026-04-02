---
title: "IT 프로젝트 이해관계자 관리 실무 — Power-Interest Grid와 RACI로 정리하는 법"
date: 2026-04-03
categories: planning-insight
tags: [이해관계자관리, Power-Interest Grid, RACI, 프로젝트관리, IT기획, PMBOK]
excerpt: "IT 프로젝트에서 이해관계자를 Power-Interest Grid로 분류하고 RACI 매트릭스로 역할을 정리하는 실무 방법을 다룬다"
---

IT 프로젝트 실패 원인의 상당수는 기술이 아니라 사람이다. PMI의 Pulse of the Profession 보고서(2021년 기준)에 따르면 프로젝트 실패 원인 1위는 요구사항 변경이고, 이해관계자 간 소통 부족이 그 뒤를 잇는다 ([PMI Pulse of the Profession](https://www.pmi.org/learning/thought-leadership/pulse)). 하이브리드 팀 환경에서 이 문제는 조기에 잡지 않으면 걷잡기 어려워진다 ([CIO Korea 이해관계자 관리 안내서](https://www.cio.com/article/3514946/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EB%8F%84-%EC%9D%B8%EC%82%AC%EA%B0%80-%EB%A7%8C%EC%82%AC%C2%B7%C2%B7%C2%B7-%EC%9D%B4%ED%95%B4%EA%B4%80%EA%B3%84%EC%9E%90-%EA%B4%80.html)). PMBOK 7판은 이해관계자를 별도 Performance Domain으로 분리했다. 기획자 입장에서 정리하면 방법론은 두 가지로 수렴한다. Power-Interest Grid와 RACI 매트릭스다.

---

## 1단계: 이해관계자 목록 작성

먼저 프로젝트에 영향을 주거나 받는 인물을 전수 나열한다. [Asana의 이해관계자 분석 가이드](https://asana.com/ko/resources/project-stakeholder)는 이름·부서·역할·연락처를 기본 4개 항목으로 권장한다. 내부 인원만이 아니라 외부 벤더, 규제 기관, 핵심 고객도 포함한다.

목록을 만들다 보면 누락자가 보인다. 운영팀이나 보안팀처럼 프로젝트 말미에 뒤늦게 개입하는 부서가 대표적이다. 착수 시점에 전부 포함하지 않으면 후반에 재작업이 생긴다.

---

## 2단계: Power-Interest Grid 배치

Power-Interest Grid는 이해관계자를 권한(Power)과 관심도(Interest) 두 축으로 4사분면에 배치하는 도구다. 각 사분면별 대응 전략이 다르다.

| 사분면 | 전략 | 소통 주기 예시 |
|--------|------|----------------|
| High Power / High Interest | Manage Closely — 핵심 의사결정자 | 주 1회 상태 공유 |
| High Power / Low Interest | Keep Satisfied — C레벨 임원 | 월 1회 핵심 요약 보고 |
| Low Power / High Interest | Keep Informed — 현업 실무자 | 변경사항 즉시 공유 |
| Low Power / Low Interest | Monitor — 간접 영향자 | 분기 1회 뉴스레터 수준 |

[Institute of Project Management 블로그의 이해관계자 관리 가이드](https://instituteprojectmanagement.com/au/blog/what-is-stakeholder-management/)는 이 4사분면 분류를 초기 기획 단계에서 완료할 것을 권고한다. 사분면이 결정되면 회의 참석 범위와 보고 단계를 설계하기 쉬워진다.

프로젝트가 진행되면서 이해관계자의 권한이나 관심도는 바뀐다. 5단계에서 다루는 분기별 재평가가 필요한 이유다.

---

## 3단계: 사분면별 소통 전략 수립

Power-Interest Grid를 완성하면 소통 전략 설계가 쉬워진다. 사분면별로 소통 채널, 내용, 주기를 다르게 가져간다.

**Manage Closely** 그룹에는 주간 보고서보다 슬랙 DM이나 5분 구두 보고가 맞는다. 의사결정 대기 시간을 줄이는 것이 핵심이다.

**Keep Satisfied** 그룹은 정보 과부하를 피해야 한다. 세부 사항 대신 예산·일정·리스크 3개 항목만 담은 대시보드로 보고한다.

**Keep Informed** 그룹은 현업 실무자가 많다. 이들에게는 변경사항이 자신의 업무에 어떤 영향을 주는지를 먼저 설명해야 한다. [CIO Korea의 이해관계자 관리 계획 4단계](https://www.cio.com/article/3517380/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B2%B0%EA%B3%BC%EC%97%90-%EB%93%9D%EC%9D%B4-%EB%90%98%EB%8A%94-%EC%9D%B4%ED%95%B4%EA%B4%80%EA%B3%84%EC%9E%90-%EA%B4%80%EB%A6%AC-%EA%B3%84%ED%9A%8D-4%EB%8B%A8.html)는 이 그룹의 저항을 줄이려면 초기 인터뷰를 통해 요구사항을 사전 수렴해야 한다고 제안한다.

---

## 4단계: RACI 매트릭스로 역할-책임 명확화

RACI 매트릭스는 태스크와 역할자를 교차해 책임을 배정하는 표다. 4개 역할로 구성된다.

- **R (Responsible)**: 실제 작업 수행자. 한 태스크에 여럿 가능하다.
- **A (Accountable)**: 최종 승인·책임자. 태스크당 반드시 1명만 지정한다.
- **C (Consulted)**: 의견을 구하는 전문가. 양방향 소통이 필요하다.
- **I (Informed)**: 결과를 통보받는 대상. 단방향 소통으로 충분하다.

[project-management.com의 RACI 매트릭스 가이드](https://project-management.com/understanding-responsibility-assignment-matrix-raci-matrix/)는 A가 2명 이상인 경우 의사결정이 지연되는 패턴이 반복된다고 지적한다. A는 반드시 1명으로 제한해야 한다.

PMBOK 7판은 RACI를 RAM(Responsibility Assignment Matrix, 책임배정 매트릭스)의 하위 형태로 위치시킨다 ([PMI PMBOK 7판 공식 가이드](https://www.pmi.org/pmbok-guide-standards/foundational/pmbok)). RAM은 프로젝트 특성에 맞게 역할을 조정할 수 있는 상위 개념이다.

RACI를 처음 작성할 때 실수가 나는 지점은 C와 I의 혼동이다. C는 의견이 결과물에 반영되어야 하는 경우다. 반영 여부가 무관하다면 I로 내려야 한다. 이 구분을 흐리면 회의가 늘고 의사결정 속도가 떨어진다.

---

## 5단계: 분기별 재평가

이해관계자 관리는 착수 시점 한 번으로 끝나지 않는다. Power-Interest Grid와 RACI는 살아있는 문서다. 분기 단위로 두 가지를 점검한다.

1. 이해관계자 권한·관심도 변동 여부 (조직 개편, 담당자 교체)
2. 태스크 신규 추가나 역할 변경에 따른 RACI 갱신

재평가 없이 초기 문서를 그대로 쓰면, 실제 의사결정권자와 문서상 의사결정권자가 달라지는 상황이 생긴다.

---

## 정리

자료를 정리하면서 확인한 점은, 이 두 도구가 서로 다른 질문에 답한다는 것이다. Power-Interest Grid는 "누구에게 얼마나 공을 들일지"를 정한다. RACI는 "각 태스크에서 누가 무엇을 하는지"를 정한다. 두 도구를 같이 쓰면 소통 낭비와 책임 공백이 줄어든다.

실무에서는 프로젝트 착수 초기에 이 두 문서를 완성하는 것이 일반적이다. 늦게 만들면 이미 고착된 소통 패턴을 바꾸기 어렵다. 다음 단계로는 소통 계획서(Communication Plan)를 연결하면 이해관계자 관리 체계가 완성된다.
