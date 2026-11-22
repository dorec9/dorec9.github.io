#!/usr/bin/env bash
# Ruby 3.1 또는 격리된 컨테이너에서 GitHub Pages 사이트를 검증한다.
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_root"

build_site() {
  # 시스템 gem과 사용자 전역 Bundler 설정을 바꾸지 않는다.
  export BUNDLE_PATH="$repo_root/vendor/bundle"
  export BUNDLE_USER_HOME="$repo_root/vendor/bundle-user"
  export BUNDLE_APP_CONFIG="$repo_root/.bundle"
  export BUNDLE_GEMFILE="$repo_root/Gemfile"
  export BUNDLE_TIMEOUT="${BUNDLE_TIMEOUT:-30}"
  if ! bundle check >/dev/null 2>&1; then
    bundle install --jobs 4 --retry 3
  fi
  bundle exec jekyll build "$@"
}

# github-pages의 Liquid 의존성은 Ruby 3.2에서 제거된 tainted?를 사용한다.
if command -v ruby >/dev/null 2>&1 && command -v bundle >/dev/null 2>&1 \
  && ruby -e 'exit(RUBY_VERSION.start_with?("3.1.") ? 0 : 1)'; then
  build_site "$@"
  exit 0
fi

if [[ "${BLOG_BUILD_CONTAINER:-}" == 1 ]]; then
  echo '오류: 빌드 컨테이너에 Ruby 3.1과 Bundler가 필요합니다.' >&2
  exit 1
fi
if ! command -v docker >/dev/null 2>&1 || [[ ! -S /var/run/docker.sock ]]; then
  echo '오류: Ruby 3.1과 Bundler 또는 로컬 Docker가 필요합니다.' >&2
  exit 1
fi

# 관리 환경의 로컬 소켓만 사용한다. 원격 Docker/TLS 설정은 상속하지 않는다.
docker_local() {
  env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS \
    -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH \
    docker -H unix:///var/run/docker.sock "$@"
}

container_user="$(id -u):$(id -g)"
docker_args=(run --rm --user "$container_user" --workdir /work
  --mount "type=bind,src=$repo_root,dst=/work"
  --env BLOG_BUILD_CONTAINER=1 --env BUNDLE_SILENCE_ROOT_WARNING=1)
# Docker 클라이언트가 컨테이너에 맞는 세션 프록시를 전달한다.
# 호스트의 proxy 별칭으로 덮어쓰면 내부 컨테이너에서 접근할 수 없다.

# 관리 환경 프록시의 CA를 전달하되 TLS 인증서 검증은 유지한다.
ca_bundle="${SSL_CERT_FILE:-/etc/ssl/certs/ca-certificates.crt}"
if [[ -f "$ca_bundle" ]]; then
  docker_args+=(--mount "type=bind,src=$ca_bundle,dst=/tmp/blog-ca-certificates.crt,readonly"
    --env SSL_CERT_FILE=/tmp/blog-ca-certificates.crt)
fi

image='ruby:3.1-bookworm@sha256:91627f55e8969006aab67d15c92fb930500ff73948803da1330b8a853fecebb5'
docker_local "${docker_args[@]}" "$image" bash scripts/build_site.sh "$@"
