#!/bin/bash
LABEL="com.agentgov.daily"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null
rm -f "$HOME/Library/LaunchAgents/$LABEL.plist"
echo "Daily schedule removed."
