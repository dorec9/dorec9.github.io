# 실패 패턴 레지스트리

실패 사례를 축적해서 규칙을 점진적으로 개선한다.

## 기록 형식
```
### YYYY-MM-DD: [실패 유형]
- 상황:
- 기대:
- 실제:
- 원인:
- 조치: (규칙 추가/수정 여부)
```

## 톤 위반

## 블랙리스트 미검출

## 소스 정책 위반

## 빌드 실패

### 2026-07-31: Ruby 3.3 + Liquid 4.0.3 tainted? 호환성 오류
- 상황: /auto-publish business-economy 실행 중 6단계(bundle exec jekyll build) 빌드 검증
- 기대: 포스트 추가 후 빌드 성공
- 실제: `Liquid Exception: undefined method 'tainted?' for nil in /_layouts/single.html` 로 빌드 실패 (NoMethodError, liquid/variable.rb:124 taint_check)
- 원인: Gemfile.lock이 github-pages gem을 통해 jekyll 3.9.0 / liquid 4.0.3에 고정. liquid 4.0.3의 assign 태그 렌더링이 `Object#tainted?`를 호출하는데, Ruby 3.2부터 이 메서드가 제거됨. `.github/workflows/*.yml`의 ruby/setup-ruby가 3.3을 사용해 발생. 새 포스트 파일을 제외하고 기존 main 상태 그대로 빌드해도 동일하게 재현되어, 콘텐츠와 무관한 CI 환경/Gemfile 버전 불일치로 확인됨
- 조치: 근본 원인은 gem 버전 고정과 CI Ruby 버전의 불일치이므로 콘텐츠 작업 범위를 벗어남. Gemfile/워크플로 수정은 사용자 확인 필요 — 자동 발행 파이프라인에서 임의 변경하지 않음. 재발 시 이 항목을 참조해 즉시 원인 규명 단계를 건너뛸 것

## 기타
