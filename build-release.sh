#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

missing=""
for var in P4A_RELEASE_KEYSTORE P4A_RELEASE_KEYALIAS P4A_RELEASE_KEYSTORE_PASSWD P4A_RELEASE_KEYALIAS_PASSWD; do
  [ -n "${!var:-}" ] || missing="$missing $var"
done
if [ -n "$missing" ]; then
  echo "build-release: missing$missing" >&2
  echo "Fill them in .env (see .env.example)." >&2
  exit 1
fi

source .venv/bin/activate

for jdk in /usr/lib/jvm/java-21-openjdk /usr/lib/jvm/java-17-openjdk; do
  if [ -d "$jdk" ]; then
    export JAVA_HOME="$jdk"
    export PATH="$JAVA_HOME/bin:$PATH"
    break
  fi
done

export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS:+$JAVA_TOOL_OPTIONS }-Djava.net.preferIPv4Stack=true"

exec buildozer android release "$@"
