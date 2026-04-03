---
title: "국가R&D 공고 자동화 에이전트를 만든 과정 — 유사 RFP 탐색·발표 스크립트 생성과 7컨테이너 배포 구성"
date: 2026-04-03
categories: [project-retrospect]
tags: [FastAPI, ChromaDB, LangGraph, Gemini, Docker, RAG, 국가RD, 기업마당, sentence-transformers, Spring Boot]
excerpt: "국가R&D 공고를 분석하고 유사 RFP를 탐색한 뒤 발표 스크립트까지 생성하는 에이전트를 팀 프로젝트로 구현했다. 내가 담당한 Step 2 유사 RFP 탐색, Step 4 발표 스크립트/Q&A 생성, 7개 서비스 Docker Compose 배포 구성에서 겪은 판단과 실패를 정리한다."
---

국가R&D 사업에 지원하려면 공고문 분석부터 발표 준비까지 반복 작업이 많다. 팀에서 이 과정을 자동화하는 에이전트를 만들었고, 나는 유사 RFP 탐색(Step 2)·발표 스크립트/Q&A 생성(Step 4)·Docker Compose 배포 구성을 담당했다. 이 글은 그 판단 근거와 실패 기록이다.

---

## 프로젝트 배경

기업마당([bizinfo.go.kr](https://www.bizinfo.go.kr/))은 중소기업 대상 정부지원 사업 공고를 RSS로 제공한다. 공고가 매주 수십 건씩 올라오는데, 기업이 자격요건을 수동으로 검토하고 유사 RFP를 찾아 제안서를 쓰는 데 1주일 이상 걸리는 경우가 많다.

Randi RD-agent는 이 흐름을 4단계로 자동화한다.

1. 공고 분석 → 체크리스트/분석 JSON
2. 유사 RFP 탐색 → 관련 사례 요약
3. PPT 생성 → LangGraph 기반 발표자료 렌더링
4. 발표 스크립트/Q&A → Gemini로 slides·qna JSON 생성

팀 4명 중 나는 Step 2, Step 4, 배포 구성을 담당했다. Step 1과 Step 3은 다른 팀원이 구현했다.

---

## 전체 아키텍처

```
Browser → Nginx → /api/* → Spring Boot :8080
                → /api/analyze/step3,4 → FastAPI :8000
```

Spring Boot는 JWT 인증·공고 관리·감사 로그를 담당한다. FastAPI는 AI 파이프라인 4단계를 처리한다. DB는 MySQL(관계형 데이터)·Redis(세션·캐시)·ChromaDB 2개(법령 벡터·전략 벡터)로 구성된다.

언어 비중은 TypeScript 8.66MB, Python 411KB, Java 221KB 순이다. 프론트엔드가 가장 무겁고, AI 파이프라인과 백엔드가 그 뒤를 잇는다.

---

## 기술 스택 선택 이유

### FastAPI를 AI 파이프라인 서버로 선택한 이유

Gemini API 호출은 I/O 대기 시간이 200ms~2s 수준으로 길다. FastAPI는 `async def` 라우트에서 이 대기 시간을 블로킹 없이 처리할 수 있다. [FastAPI 공식 문서](https://fastapi.tiangolo.com/async/)에 따르면 `async`/`await` 기반 경로는 Starlette의 비동기 루프 위에서 실행돼 I/O 대기 중 다른 요청을 처리할 수 있다.

반면 Spring Boot WebFlux도 비동기를 지원하지만, Python AI 라이브러리(sentence-transformers, torch, LangGraph)와 통합할 때 FFI 오버헤드가 생긴다. FastAPI로 AI 파이프라인을 분리하면 Spring이 비즈니스 로직에 집중할 수 있다.

### ChromaDB를 벡터 저장소로 선택한 이유

법령 텍스트와 기업 전략 문서를 임베딩해 RAG를 구성해야 했다. [ChromaDB 공식 문서](https://docs.trychroma.com/)는 pip 설치 후 Python-native로 바로 사용 가능하고, sentence-transformers와 기본 통합을 제공한다. Pinecone은 외부 API 의존도가 높고, FAISS는 영속성 관리를 직접 해야 한다([facebookresearch/faiss](https://github.com/facebookresearch/faiss)). 팀 규모(4명)와 일정(약 2개월)을 고려해 ChromaDB를 선택했다.

ChromaDB를 법령용·전략용 2개 컨테이너로 분리한 이유는 컬렉션 혼용 시 쿼리 정밀도가 낮아질 수 있다는 판단이었다. 법령 데이터는 정형화된 조문 텍스트이고, 전략 문서는 비정형 서술이어서 임베딩 분포가 다를 것으로 봤다.

---

## Step 2: 유사 RFP 탐색 — 두 트랙 병렬 탐색

### 설계

`search_two_tracks` 함수는 두 경로로 동시에 검색한다.

- **Track A**: 법령 ChromaDB에서 자격요건 관련 조문 검색
- **Track B**: 전략 ChromaDB에서 과거 유사 공고 사례 검색

두 결과를 합쳐 Gemini에 프롬프트로 전달하면 "이 공고와 유사한 사례"를 자연어로 요약한다.

### 실제로 겪은 문제

Track A와 Track B 결과 품질이 불균일했다. 법령 ChromaDB는 조문 단위로 청킹해 임베딩했는데, 너무 짧은 청크(1~2문장)는 문맥이 없어 유사도 점수가 낮게 나왔다. 청크 크기를 256 토큰에서 512 토큰으로 늘리고 overlap을 64 토큰으로 설정하자 상위 5건에서 관련 없는 조문이 사라졌다.

Track B는 과거 공고 데이터가 충분하지 않아 결과가 빈약했다. 데이터 양 부족 문제는 에이전트 설계로 해결할 수 없어서, 프롬프트에 "유사 사례가 부족할 경우 공고 유형과 일반적인 R&D 사업 특성을 기반으로 추론"이라는 지시를 추가했다. 근본 해결은 아니지만 출력이 빈 응답보다는 나았다.

### sentence-transformers 모델 선택

기본 `all-MiniLM-L6-v2`는 영어 최적화 모델이다. 한국어 법령 텍스트에 적용했을 때 유사도 점수 분포가 좁았다. `jhgan/ko-sroberta-multitask`로 교체했을 때 상위 3건 중 관련 법령 비율이 높아졌다. 다만 모델 크기가 커서 컨테이너 초기 로딩 시간이 약 30초 늘었다.

---

## Step 4: 발표 스크립트·Q&A 생성

### 입력과 출력

Step 3에서 PPT가 생성되면 Step 4는 그 텍스트를 추출한 뒤 Gemini에 전달해 두 가지 JSON을 생성한다.

- `slides`: 슬라이드별 발표 스크립트
- `qna`: 예상 질문과 답변 쌍

### 프롬프트 설계에서 판단한 것

슬라이드 수가 가변적이다. 10장일 수도 있고 30장일 수도 있다. 프롬프트에 슬라이드 수를 동적으로 주입하고, 출력 JSON 스키마를 명시했다. Gemini가 스키마를 무시하고 마크다운 텍스트로 응답하는 경우가 초반에 자주 발생했다.

해결책은 두 단계였다. 첫째, `response_mime_type: "application/json"`을 API 파라미터로 설정해 Gemini가 JSON만 반환하도록 강제했다. 둘째, 응답을 파싱할 때 try/except로 감싸고 실패 시 원본 텍스트와 함께 오류를 로그에 남겼다. 이 두 조치로 파싱 실패율이 약 80%에서 5% 미만으로 줄었다.

### Q&A 품질 문제

Gemini가 생성하는 예상 질문이 너무 일반적이었다. "연구 목표가 무엇인가요?" 같은 수준이었다. 프롬프트에 공고문의 핵심 평가 기준을 명시적으로 포함시키자 질문이 구체화됐다. "사업화 기간 내 매출 달성 근거는?" 같은 수준으로 바뀌었다.

---

## 배포 구성: Docker Compose 7개 서비스

### 서비스 목록

```
nginx, spring, fastapi, mysql, redis, chroma_law, chroma_strategy
```

### 설계 판단

**의존성 순서**: mysql·redis·chroma_law·chroma_strategy가 준비된 뒤 spring과 fastapi가 시작해야 한다. `depends_on`만으로는 부족해서 spring 컨테이너에 헬스체크 스크립트를 추가했다. MySQL이 실제로 연결 가능한 상태인지 확인한 뒤 Spring을 기동하는 방식이다.

**네트워크 분리**: 외부에 노출되는 서비스는 nginx뿐이다. spring·fastapi·mysql·redis·chroma 컨테이너는 내부 브리지 네트워크에만 있다. 개발 환경에서 포트를 열어 디버깅하다가 배포 직전에 포트 매핑을 닫는 것을 잊는 실수를 방지하려고 docker-compose.override.yml을 따로 관리했다.

**ChromaDB 영속성**: 두 ChromaDB 컨테이너 모두 호스트 볼륨을 마운트했다. 컨테이너를 재시작해도 임베딩 데이터가 유지된다. 초기에 볼륨을 설정하지 않아 컨테이너 재시작마다 ChromaDB를 다시 인덱싱해야 했다. 법령 데이터 인덱싱에 약 12분이 걸렸기 때문에 이 실수는 바로 티가 났다.

### Nginx 라우팅

```
/api/*               → spring:8080
/api/analyze/step3   → fastapi:8000
/api/analyze/step4   → fastapi:8000
```

Step 3·4만 FastAPI로 라우팅하고 나머지는 Spring으로 보낸다. Step 1·2는 Spring이 FastAPI를 내부적으로 호출하는 방식으로 처리한다.

---

## 배운 것과 개선할 점

**임베딩 모델은 도메인을 먼저 확인해야 한다.** `all-MiniLM-L6-v2`는 영어 우선 모델이라 한국어 법령 텍스트에 바로 쓰면 검색 품질이 낮다. 프로젝트 초반에 모델 선택에 30분이라도 더 썼다면 중반의 디버깅 시간 2일을 아꼈을 것이다.

**LLM 출력 포맷은 API 파라미터로 강제하는 게 프롬프트 조정보다 낫다.** 프롬프트로 JSON 형식을 유도하는 방법은 모델 버전이 바뀌면 깨진다. `response_mime_type`처럼 API가 지원하는 파라미터를 먼저 확인하는 습관이 필요하다.

**Docker Compose 의존성 관리는 헬스체크가 핵심이다.** `depends_on: condition: service_healthy`를 쓰려면 각 서비스에 `healthcheck`를 정의해야 한다. 이 설정을 처음부터 넣었다면 초기 기동 순서 문제로 디버깅한 4시간을 줄일 수 있었다.

개선 여지가 있는 부분은 Track B 데이터 부족 문제다. 기업마당 RSS를 지속적으로 파싱해 과거 공고를 축적하면 유사 RFP 탐색 품질이 올라간다. 지금은 초기 데이터셋이 작아 결과가 빈약하다.

---

레포지토리는 [dorec9/Randi_RD-agent](https://github.com/dorec9/Randi_RD-agent)에 있다.
