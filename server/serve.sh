#!/bin/bash
set -euo pipefail

LABEL="com.openclaw.deploy-station"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
PORT=8080
PUBLIC_DIR="$(cd "$(dirname "$0")/../public" && pwd)"

echo "=== Deploy Station ==="
echo "Serving: $PUBLIC_DIR"
echo "Port:    $PORT"

# Create or update launchd plist
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>-m</string>
        <string>http.server</string>
        <string>${PORT}</string>
        <string>--directory</string>
        <string>${PUBLIC_DIR}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${HOME}/.nakedcode/logs/deploy-station.log</string>
    <key>StandardErrorPath</key>
    <string>${HOME}/.nakedcode/logs/deploy-station.error.log</string>
</dict>
</plist>
EOF

echo "Plist written: $PLIST"

# Unload if already loaded (ignore errors if not loaded)
launchctl unload "$PLIST" 2>/dev/null || true

# Load the service — launchd starts the process automatically (RunAtLoad + KeepAlive)
launchctl load "$PLIST"

# Wait for server to come up
sleep 2
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
  echo ""
  echo "Server draait. Bereikbaar op:"
  echo "  http://localhost:${PORT}"
  echo "  http://mini.local:${PORT}"
  echo ""
  echo "De server start voortaan automatisch bij login."
else
  echo ""
  echo "Launchd service geladen, maar server reageert nog niet (HTTP $HTTP_CODE)."
  echo "Check logs: ~/.nakedcode/logs/deploy-station.error.log"
fi
