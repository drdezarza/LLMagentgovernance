#!/bin/bash
# Runs one time-boxed session (length from config/settings.yaml unless --hours is given).
# Extra arguments go to `python -m agentgov run`, e.g.  scripts/run_session.sh --hours 1   or   --mock --hours 0.5
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1
mkdir -p logs
if [ "$1" = "--selftest" ]; then date > logs/selftest.ok; exit 0; fi
for v in .venv .venv.nosync; do [ -f "$v/bin/activate" ] && source "$v/bin/activate" && break; done
KEEP_AWAKE=""
command -v caffeinate >/dev/null 2>&1 && KEEP_AWAKE="caffeinate -i -s"      # macOS: keep the machine awake
$KEEP_AWAKE python -m agentgov run "$@" >> logs/daily.log 2>&1
STATUS=$?
if command -v osascript >/dev/null 2>&1; then
  osascript -e "display notification \"Session finished (exit $STATUS)\" with title \"agentgov\"" 2>/dev/null || true
fi
exit $STATUS
