---
name: write-post
description: 블로그 포스트 생성. 주제를 받아 리서치 후 _posts/에 마크다운 파일 작성
argument-hint: [주제]
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# 블로그 포스트 작성

## 입력
- `$ARGUMENTS`: 포스트 주제

## 프로세스
1. 주제 리서치 (WebSearch로 최신 데이터/사례 수집)
2. 아웃라인 구성 (3-7개 섹션)
3. 본문 작성 (1,500~3,000자)
4. front matter 생성
5. `_posts/YYYY-MM-DD-slug.md`로 저장

## front matter 템플릿
```yaml
---
title: "제목"
date: YYYY-MM-DD
categories: category-slug
tags: [태그1, 태그2, 태그3]
excerpt: "한 줄 요약 (100자 이내)"
---
```

## 카테고리 슬러그
- project-retrospect, planning-insight, data-statistics
- trend-research, business-economy, harness-engineering

## 파일명 규칙
- `_posts/YYYY-MM-DD-영문-소문자-하이픈-구분.md`

## 규칙
- `.claude/rules/`의 tone, blacklist, source-policy 규칙 필수 준수
- 모든 주장에 데이터/소스 근거 포함
- 과장 표현 절대 불가
- ~다 체로 통일
