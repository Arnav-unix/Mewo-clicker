#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

source .venv/bin/activate

for jdk in /usr/lib/jvm/java-21-openjdk /usr/lib/jvm/java-17-openjdk; do
  if [ -d "$jdk" ]; then
    export JAVA_HOME="$jdk"
    export PATH="$JAVA_HOME/bin:$PATH"
    break
  fi
done

export JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS:+$JAVA_TOOL_OPTIONS }-Djava.net.preferIPv4Stack=true"

exec buildozer android debug "$@"
