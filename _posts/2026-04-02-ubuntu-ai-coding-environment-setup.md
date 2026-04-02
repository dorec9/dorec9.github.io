---
title: "Ubuntu 24.04에서 AI 코딩 환경 구축하기 — Ghostty + tmux + Claude Code"
date: 2026-04-02
categories: harness-engineering
tags: [Ubuntu, Ghostty, tmux, Claude-Code, 환경구축]
excerpt: "블로그 자동화 하네스를 위한 개발 환경을 Ghostty, tmux, Claude Code 조합으로 세팅한 과정을 정리했다."
---

## 왜 이 조합인가

블로그 자동화 하네스 시스템을 구축하기 위해 개발 환경부터 세팅했다.
선택한 도구 3가지와 선택 이유:

| 도구 | 역할 | 선택 이유 |
|------|------|-----------|
| Ghostty | 터미널 에뮬레이터 | GPU 가속, 네이티브 탭/분할, 300+ 내장 테마, 하네스 엔지니어링 명명자 Mitchell Hashimoto가 직접 개발 |
| tmux | 터미널 멀티플렉서 | 세션 유지(detach/attach), SSH 끊어져도 작업 보존, 화면 분할 |
| Claude Code | AI 코딩 에이전트 | 터미널 기반, 프로젝트 전체 맥락 이해, CLAUDE.md/Skills/Hooks로 하네스 설계 가능 |

Ghostty는 로컬 터미널 환경, tmux는 세션 관리와 화면 분할, Claude Code는 AI 에이전트.
세 도구가 각자 역할이 달라서 경쟁이 아니라 보완 관계다.

---

## 1. 사전 준비

Ubuntu 24.04 LTS 기본 상태에서 curl과 git이 없었다.

```bash
sudo apt update && sudo apt install curl git -y
```

확인:

```bash
curl --version   # 8.5.0
git --version    # 2.43.0
```

---

## 2. Ghostty 설치

### 설치 방법 선택

Ghostty는 공식 사전 빌드 바이너리를 macOS에만 제공한다.
Ubuntu에서는 4가지 방법이 있는데, 커뮤니티 PPA가 가장 편리하다.

| 방법 | 장점 | 단점 |
|------|------|------|
| **PPA (선택)** | apt로 자동 업데이트, 3줄 설치 | 커뮤니티 관리 |
| Snap | 간편 | Nvidia 환경에서 시작 느림 보고 있음 |
| AppImage | 범용 | 자동 업데이트 없음 |
| 소스 빌드 | 최신 버전 | Zig 0.15.2 필요, 복잡 |

### 설치 실행

```bash
sudo add-apt-repository ppa:mkasberg/ghostty-ubuntu
sudo apt update
sudo apt install ghostty
```

### 설정 파일 생성

Ghostty는 제로 설정 철학이라 설정 파일 없이도 동작하지만, 커스터마이징을 위해 직접 만들었다.

```bash
mkdir -p ~/.config/ghostty
nano ~/.config/ghostty/config
```

파일 이름이 `config`다. 확장자 없음.

```ini
# 창 테마 (다크 모드)
window-theme = dark

# 테마 (다크/라이트 자동 전환)
theme = dark:Catppuccin Mocha,light:Catppuccin Latte

# 탭 전환 (Super+좌/우)
keybind = super+left=previous_tab
keybind = super+right=next_tab

# 분할 구분선 색상
split-divider-color = #ff6600
```

### 설정 확인

설정이 제대로 적용됐는지 확인:

```bash
ghostty +show-config 2>&1 | head -20
```

**주의:** 설정 변경 후 반드시 Ghostty 창에서 확인해야 한다.
기존 GNOME Terminal에서는 아무리 바꿔도 변화가 없다.

```bash
# 지금 어떤 터미널인지 확인
echo $TERM
# xterm-ghostty → Ghostty
# xterm-256color → GNOME Terminal 등 다른 터미널
```

### 유용한 CLI 명령어

```bash
ghostty +list-themes          # 내장 테마 미리보기
ghostty +list-fonts           # 사용 가능 폰트 목록
ghostty +show-config --default --docs  # 모든 설정 옵션 + 설명
```

### 핵심 단축키

| 동작 | 단축키 |
|------|--------|
| 새 탭 | Ctrl+Shift+T |
| 수평 분할 (아래로) | Ctrl+Shift+E |
| 수직 분할 (오른쪽으로) | Ctrl+Shift+O |
| 분할 패인 이동 | Ctrl+Alt+방향키 |
| 스크롤백 검색 | Ctrl+Shift+F |
| 설정 리로드 | Ctrl+Shift+, |
| 복사 / 붙여넣기 | Ctrl+Shift+C / Ctrl+Shift+V |

---

## 3. tmux 설치 및 설정

### 설치

Ubuntu 24.04 공식 저장소에 포함되어 있어서 한 줄이면 된다.

```bash
sudo apt install tmux -y
tmux -V   # tmux 3.4
```

### 설정 파일 작성

복사/붙여넣기 편의성과 직관적인 키바인딩에 초점을 맞췄다.

시스템 클립보드 연동을 위해 xclip 먼저 설치:

```bash
sudo apt install xclip -y
```

설정 파일 생성:

```bash
nano ~/.tmux.conf
```

```bash
# ── 프리픽스: Ctrl+a (Ctrl+b보다 손이 편함) ──
set-option -g prefix C-a
unbind C-b
bind C-a send-prefix

# ── 마우스 ──
set -g mouse on

# ── 복사/붙여넣기 (시스템 클립보드 연동) ──
setw -g mode-keys vi

# 마우스 드래그 → 자동 복사
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# v로 선택 시작, y로 복사 (vim 스타일)
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# Ctrl+v로 붙여넣기
bind C-v run "xclip -selection clipboard -o | tmux load-buffer - && tmux paste-buffer"

# ── 화면 분할 (직관적) ──
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# ── 패인 이동 (Alt+방향키, 프리픽스 없이) ──
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# ── 기본 설정 ──
set -g base-index 1
setw -g pane-base-index 1
set -g history-limit 10000
set -g default-terminal "screen-256color"

# ── 설정 리로드 ──
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# ── Ghostty 호환 ──
set -s extended-keys on
set -s extended-keys-format csi-u
```

설정 적용:

```bash
tmux kill-server
tmux
```

### 복사/붙여넣기 사용법

가장 편한 방법: 마우스 드래그로 텍스트 선택 → 손 떼면 자동 클립보드 복사 → Ctrl+Shift+V로 붙여넣기.

tmux 안에서 복사한 내용을 브라우저 등 외부 앱에 Ctrl+V로 붙여넣기도 가능하다.

### 핵심 단축키 (프리픽스: Ctrl+a)

| 동작 | 단축키 |
|------|--------|
| 수직 분할 (좌/우) | Ctrl+a → \| |
| 수평 분할 (위/아래) | Ctrl+a → - |
| 패인 이동 | Alt+방향키 (프리픽스 없이) |
| 새 윈도우 | Ctrl+a → c |
| 다음 윈도우 | Ctrl+a → n |
| 세션 분리 (백그라운드) | Ctrl+a → d |
| 세션 재접속 | tmux attach |
| 설정 리로드 | Ctrl+a → r |

---

## 4. Claude Code 설치

### 설치

2026년 기준, Anthropic 공식 권장은 네이티브 인스톨러다.
Node.js 의존성 없이 단일 명령으로 설치되고, 자동 업데이트가 내장되어 있다.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

설치 완료 후 PATH 설정이 필요했다:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

확인:

```bash
claude --version   # 2.1.90 (Claude Code)
```

### 로그인

```bash
claude
```

처음 실행하면 브라우저가 열리면서 Anthropic 로그인 화면이 나온다.
Pro, Max, Teams, Enterprise 중 하나의 유료 플랜이 필요하다.

### 진단

```bash
claude doctor
```

정상 출력:

```
Diagnostics
  └ Currently running: native (2.1.90)
  └ Config install method: native
  └ Search: OK (bundled)
Updates
  └ Auto-updates: enabled
```

**주의:** `claude doctor`는 Claude Code 세션 밖에서 실행해야 한다.
세션 안에서는 동작하지 않으므로, `/exit`으로 나간 후 일반 터미널에서 실행.

### 프로젝트 초기화

```bash
mkdir -p ~/blog-harness
cd ~/blog-harness
git init
git branch -m main
git config --global init.defaultBranch main
```

### CLAUDE.md 생성

Claude Code 세션에서 직접 생성을 지시했다:

```bash
cd ~/blog-harness
claude
```

생성된 CLAUDE.md 핵심 내용:

```markdown
# Blog Automation Harness

## Project
- 취업용 기술 블로그 (경영기획/IT기획 타겟)
- GitHub Pages + Jekyll 기반
- 하네스 엔지니어링으로 AI 에이전트 블로그 자동화 설계

## Rules
- IMPORTANT: 한국어 작성, 실무자 시점
- IMPORTANT: 과장 표현 금지
- YOU MUST: 모든 주장에 데이터/소스 근거 포함
- 커밋 메시지 한국어

## Categories (6개)
1. 프로젝트 회고
2. 경영기획·IT기획 직무 인사이트
3. 데이터 분석/통계
4. 업계 트렌드 리서치
5. 경영·경제 분석
6. AI 하네스 엔지니어링 설계 일지
```

---

## 5. 세 도구 통합 워크플로우

```bash
# 1. Ghostty에서 tmux 세션 시작
tmux new -s harness

# 2. 수직 분할
# Ctrl+a → |

# 3. 왼쪽 패인: Claude Code
cd ~/blog-harness && claude

# 4. Alt+오른쪽 (오른쪽 패인으로 이동)
# 오른쪽 패인: 파일 확인, git, 빌드 등 일반 작업

# 5. 작업 중단 시
# Ctrl+a → d (세션 분리, 백그라운드 유지)

# 6. 다시 돌아올 때
tmux attach -t harness
```

---

## 다음 단계

환경 구축이 완료되었다. 다음은:

- GitHub Pages + Jekyll 블로그 초기 세팅 (minimal-mistakes 테마, air 스킨)
- 6개 카테고리 페이지 생성
- 첫 번째 포스트 발행
