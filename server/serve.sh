#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PORT=8080
PLIST="$HOME/Library/LaunchAgents/com.deploystation.server.plist"

mkdir -p "$HOME/Library/LaunchAgents"

# Schrijf launchd plist
cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.deploystation.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_DIR/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/access.log</string>
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/error.log</string>
</dict>
</plist>
EOF

echo "Plist geschreven: $PLIST"

# Laad of herlaad de service
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "Deploy Station draait op http://localhost:$PORT"
echo "Launchd service geregistreerd — start automatisch bij login"
