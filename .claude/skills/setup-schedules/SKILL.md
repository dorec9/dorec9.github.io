---
name: setup-schedules
description: 5개 카테고리의 자동 발행 cron 스케줄을 일괄 등록한다
allowed-tools: CronCreate, CronList, CronDelete
---

# 스케줄 일괄 등록

## 프로세스

### 1단계: 기존 스케줄 확인
- `CronList`로 현재 등록된 스케줄 목록을 확인한다
- 이미 동일한 cron이 등록되어 있으면 해당 건은 건너뛴다

### 2단계: 스케줄 등록
다음 5개 cron job을 `CronCreate`로 등록한다:

| 카테고리 | cron 표현식 | 실행 시각 | prompt |
|---------|------------|----------|--------|
| planning-insight | `23 8 * * 1-5` | 평일 08:23 | `/auto-publish planning-insight` |
| data-statistics | `47 9 * * 1-5` | 평일 09:47 | `/auto-publish data-statistics` |
| trend-research | `13 11 * * 1-5` | 평일 11:13 | `/auto-publish trend-research` |
| business-economy | `53 12 * * 1-5` | 평일 12:53 | `/auto-publish business-economy` |
| project-retrospect | `37 14 * * 1` | 월요일 14:37 | `/repo-retrospect` |

### 3단계: 등록 결과 확인
- `CronList`로 등록된 5건의 스케줄을 확인한다
- 결과를 사용자에게 출력한다

## 참고
- 각 job 사이에 1시간 이상 간격 (동시 실행에 의한 git 충돌 방지)
- 정각(:00, :30) 의도적 회피
- Claude Code REPL 세션이 실행 중이어야 cron이 동작한다
- tmux에서 Claude Code를 상시 실행하여 유지한다
