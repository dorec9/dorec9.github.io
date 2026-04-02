---
name: publish
description: 블로그 포스트를 Git commit + push로 발행. 빌드 검증 후 커밋
argument-hint: [커밋메시지]
disable-model-invocation: true
allowed-tools: Bash, Read, Glob
---

# 블로그 발행

## 입력
- `$ARGUMENTS`: 커밋 메시지 (선택). 없으면 최근 변경된 포스트 제목으로 자동 생성

## 프로세스
1. `git status`로 변경 사항 확인
2. `bundle exec jekyll build`로 빌드 검증
3. 빌드 실패 시 **중단** + 에러 출력
4. 변경된 파일 `git add`
5. 한국어 커밋 메시지로 `git commit`
6. push 여부를 사용자에게 확인 후 실행

## 커밋 메시지 형식
```
글 발행: [포스트 제목]
```
또는
```
블로그 업데이트: [변경 내용 요약]
```

## 안전 장치
- 빌드 실패 시 절대 커밋하지 않는다
- push 전 반드시 사용자 확인
- force push 절대 불가
