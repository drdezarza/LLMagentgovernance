#!/bin/bash
# Schedule the session every day at HH:MM (default 09:00) with launchd. If the Mac is asleep at that
# time, launchd runs it at the next wake. Remove with scripts/uninstall_daily.sh.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIME="${1:-09:00}"; H=$((10#${TIME%%:*})); M=$((10#${TIME##*:}))
LABEL="com.agentgov.daily"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/logs"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$ROOT/scripts/run_session.sh</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>$H</integer><key>Minute</key><integer>$M</integer></dict>
  <key>StandardOutPath</key><string>$ROOT/logs/launchd.out</string>
  <key>StandardErrorPath</key><string>$ROOT/logs/launchd.err</string>
  <key>ProcessType</key><string>Background</string>
</dict></plist>
PL
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "✓ Scheduled daily at $(printf %02d:%02d $H $M)."
# macOS privacy check: can a launchd job write into ~/Documents?
rm -f "$ROOT/logs/selftest.ok"
TEST="$HOME/Library/LaunchAgents/$LABEL.selftest.plist"
sed -e "s#<string>$LABEL</string>#<string>$LABEL.selftest</string>#" \
    -e "s#run_session.sh</string></array>#run_session.sh</string><string>--selftest</string></array>#" \
    -e '/StartCalendarInterval/d' "$PLIST" > "$TEST"
launchctl bootout "gui/$(id -u)/$LABEL.selftest" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$TEST"; launchctl kickstart "gui/$(id -u)/$LABEL.selftest" 2>/dev/null
sleep 6
launchctl bootout "gui/$(id -u)/$LABEL.selftest" 2>/dev/null; rm -f "$TEST"
if [ -f "$ROOT/logs/selftest.ok" ]; then
  echo "✓ Background access to Documents works."
else
  echo "⚠ macOS blocked the background job from reading ~/Documents."
  echo "  Fix: System Settings → Privacy & Security → Full Disk Access → + → press Cmd+Shift+G, type /bin/bash, add it."
  echo "  (If you click 'Allow' on a pop-up instead, that also works.) Then re-run this script to re-test."
fi
