#!/bin/bash
set -e

PROJECT_DIR="/projects/deploy-station"
PUBLIC_DIR="$PROJECT_DIR/public"
PORT=8080
PLIST="$HOME/Library/LaunchAgents/com.deploystation.server.plist"

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
        <string>-m</string>
        <string>http.server</string>
        <string>$PORT</string>
        <string>--directory</string>
        <string>$PUBLIC_DIR</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/server/access.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/server/error.log</string>
</dict>
</plist>
EOF

# Laad of herlaad de service
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "✓ Deploy Station draait op http://localhost:$PORT"
echo "✓ Launchd service geregistreerd — start automatisch bij login"
