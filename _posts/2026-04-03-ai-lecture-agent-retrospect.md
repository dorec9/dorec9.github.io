---
title: "PPT를 강의 영상으로 바꾸는 AI 에이전트를 만든 과정 — LangGraph 선형 파이프라인과 설계 판단"
date: 2026-04-03
categories: [project-retrospect]
tags: [LangGraph, Gemini, GoogleCloudTTS, MoviePy, Gradio, AI에이전트, 멀티모달, 강의자동화]
excerpt: "PPT 파일을 넣으면 슬라이드 분석, 대본 생성, 음성 합성, 영상 렌더링까지 자동으로 수행하는 시스템을 LangGraph로 만들었다. 면접 에이전트와 달리 조건 분기 없는 선형 구조를 선택한 이유와 코드에서 발견한 문제들을 기록한다."
---

KT AIVLE School 프로젝트로 만든 AI 강의 에이전트다.  
목표는 하나였다. PPT 파일 하나를 업로드하면 사람이 추가로 개입하지 않아도 강의 영상 파일이 나오는 것.  
[GitHub 레포](https://github.com/dorec9/AI-Lecture-Agent)에 전체 코드가 공개되어 있다.

---

## 1. 프로젝트 배경과 목적

강의 영상을 만드는 과정에는 반복 작업이 많다.  
슬라이드 내용을 읽고 대본을 쓰고, 음성으로 녹음하고, 영상을 편집한다.  
이 흐름은 구조가 고정되어 있다. 자동화하기 적합한 형태다.

직전 프로젝트인 AI 면접 시뮬레이터는 사용자 답변에 따라 질문 흐름이 달라지는 조건 분기 구조였다.  
강의 에이전트는 달랐다. 슬라이드 순서가 정해져 있고, 각 단계는 이전 단계의 출력을 받아 처리한다.  
분기가 없으니 파이프라인 구조를 선택했다.

---

## 2. 기술 스택과 선택 이유

| 구성요소 | 선택 기술 | 이유 |
|---|---|---|
| LLM + 슬라이드 분석 | Gemini 1.5 Flash | 텍스트·이미지·표를 동시에 처리하는 멀티모달 모델 |
| 에이전트 오케스트레이션 | LangGraph | 상태 기반 워크플로우로 각 단계 입출력 추적 |
| 음성 합성 | Google Cloud TTS | Gemini와 같은 Google 생태계, API 품질 검증됨 |
| 영상 합성 | MoviePy | 파이썬에서 슬라이드 이미지 + 오디오 합성 처리 |
| UI | Gradio | 파일 업로드·영상 출력 인터페이스를 코드 몇 줄로 구성 |

Gemini 1.5 Flash를 선택한 이유는 입력 형태에 있다.  
PPT 슬라이드에는 텍스트뿐 아니라 표, 그림, 차트가 섞여 있다.  
텍스트만 처리하는 모델은 시각 정보를 분석하지 못한다.  
Gemini 1.5 Flash는 텍스트와 이미지를 하나의 프롬프트로 받는다 ([Google Gemini 공식 문서](https://ai.google.dev/gemini-api/docs/models)).  
슬라이드를 이미지로 변환해 넘기면 시각 정보까지 분석 대상에 포함된다.

LangGraph는 상태 기반 에이전트 오케스트레이션 프레임워크다 ([LangGraph 공식 문서](https://www.langchain.com/langgraph)).  
단계가 3개뿐인 선형 파이프라인에도 굳이 LangGraph를 쓴 이유가 있다.  
각 단계의 입출력을 `TypedDict`로 명시하면 어느 단계에서 데이터가 누락되는지 바로 추적할 수 있다.  
단순 함수 호출 체인으로 만들면 중간 상태를 로깅하기 위해 별도 코드가 필요하다.

---

## 3. 핵심 설계 판단

### 3-1. 선형 파이프라인 선택

이 프로젝트의 그래프 구조는 단방향이다.

```
PPT 업로드
  → analyze (슬라이드 분석)
  → generate_script (강의 대본 생성)
  → synthesize (음성 합성 + 영상 렌더링)
  → 영상 출력
```

`main.py`의 그래프 정의가 이 구조를 그대로 반영한다.

```python
workflow = StateGraph(State)
workflow.add_node("analyze", analyze_ppt_node)
workflow.add_node("generate_script", generate_script_node)
workflow.add_node("synthesize", synthesize_media_node)
workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "generate_script")
workflow.add_edge("generate_script", "synthesize")
workflow.add_edge("synthesize", END)
```

조건 분기(`add_conditional_edges`)가 없다. 이전 AI 면접 에이전트와 다른 점이다.  
면접은 "이 답변의 점수가 낮으면 심화질문을 추가한다"는 분기가 필요했다.  
강의는 다르다. 슬라이드 분석이 끝나면 대본을 생성하고, 대본이 끝나면 합성한다.  
흐름이 고정되어 있으면 선형이 적합하다. 분기를 억지로 넣을 이유가 없다.

### 3-2. TypedDict 상태 설계

`state.py`에서 파이프라인 전체 상태를 7개 필드로 정의했다.

```python
class State(TypedDict):
    ppt_path: str
    image_paths: List[str]
    ppt_analysis: List[str]
    scripts: List[str]
    audio_paths: List[str]
    final_video_path: Optional[str]
    status: str
```

각 필드가 어느 노드에서 채워지는지 추적할 수 있다.

- `ppt_path`: 사용자 입력, 초기값
- `image_paths`: analyze 노드에서 슬라이드 이미지 변환 후 채워짐
- `ppt_analysis`: analyze 노드에서 Gemini 분석 결과
- `scripts`: generate_script 노드에서 생성
- `audio_paths`: synthesize 노드에서 Google Cloud TTS 결과
- `final_video_path`: synthesize 노드 종료 시 MoviePy 렌더링 결과
- `status`: 진행 상태 문자열

`Optional[str]`로 선언된 `final_video_path`는 마지막 노드까지 실행이 완료되어야 채워진다.  
에러가 나면 `None`으로 남아 있어서 어느 단계까지 성공했는지 판단할 수 있다.

### 3-3. 노트북·모듈 이중 구조

레포의 주 개발 환경은 Jupyter Notebook이다.  
`notebooks/최종본_AI_강사_Agent_v2.ipynb` 파일이 524,812 바이트다.  
`src/` 디렉토리의 모듈 코드(`state.py`, `nodes.py`, `main.py`)는 합쳐서 2,397 바이트다.

노트북이 실험 환경이고, `src/`가 정리된 구현체다.  
노트북에서 단계별로 검증하고, 검증된 로직을 모듈로 분리했다는 흔적이 코드에 남아 있다.  
이 구조는 재현성 측면에서 유리하다. 노트북은 셀 단위 실행 상태가 환경에 따라 달라질 수 있다.  
`src/main.py`를 진입점으로 삼으면 노트북 없이도 파이프라인을 실행할 수 있다.

---

## 4. 배운 점과 개선할 점

### 발견한 문제: README와 코드의 LLM 불일치

커밋 이력에 "Update LLM reference from Google Gemini to GPT 4o-mini"라는 메시지가 있다.  
그러나 `nodes.py`에는 `google.generativeai`의 `GenerativeModel('gemini-1.5-flash')`가 그대로 남아 있다.  
README는 GPT-4o-mini라고 적혀 있고 코드는 Gemini를 쓴다.

이 불일치는 문서와 코드를 별도로 관리할 때 생기는 전형적인 드리프트(drift)다.  
운영 환경에서 이런 불일치는 온보딩 혼란이나 잘못된 API 키 설정으로 이어진다.  
LLM 교체 작업이라면 코드와 문서를 같은 커밋에 함께 반영하는 게 맞다.

### 선형 파이프라인의 한계

선형 구조는 슬라이드 품질에 그대로 노출된다.  
분석 단계에서 슬라이드당 추출 텍스트가 짧으면 대본도 그에 비례해 빈약해지고, 영상도 그 상태로 완성된다.  
중간 검증 노드가 없어서 파이프라인이 끝날 때까지 품질을 알 수 없다.

개선 방향은 두 가지다.  
첫째, 분석 결과에 대한 검증 노드를 `analyze`와 `generate_script` 사이에 추가한다.  
분석 텍스트 길이나 키워드 밀도 같은 기준으로 재시도 여부를 판단할 수 있다.  
둘째, 슬라이드 단위 처리를 병렬로 전환한다.  
현재 구조는 슬라이드를 순차 처리한다.  
LangGraph의 `Send` API를 쓰면 슬라이드별 분석과 대본 생성을 병렬로 실행할 수 있다 ([LangGraph Send API 문서](https://langchain-ai.github.io/langgraph/concepts/low_level/#send)).

### 노트북에서 모듈로 전환할 때

524KB 노트북을 2.4KB 모듈로 정리하는 과정에서 어떤 로직을 남기고 어떤 실험 코드를 버릴지 판단해야 한다.  
노트북은 실행 순서에 의존하는 변수가 섞여 있어서 그대로 함수로 옮기면 전역 변수 문제가 생긴다.  
각 노드 함수가 상태만 받아서 상태를 반환하는 구조를 유지하면 이 문제를 피할 수 있다.  
`nodes.py`의 3개 함수(`analyze_ppt_node`, `generate_script_node`, `synthesize_media_node`)가 이 원칙을 따르고 있다.

---

선형 파이프라인은 설계가 단순하지만, 단순한 만큼 각 노드의 출력 품질에 전체가 달려 있다.  
검증 없는 선형 구조는 실패를 늦게 발견한다는 걸 이 프로젝트 코드 분석으로 확인했다.  
다음 버전에서는 분석 품질 검증 노드와 병렬 처리를 붙이는 게 우선 과제다.
