# Deploy Station

## Starten
```bash
bash /projects/deploy-station/server/serve.sh
```

## Bereikbaar op
http://localhost:8080 of http://mini.local:8080 (vanuit LAN)

## Automatisch starten
serve.sh registreert zichzelf als launchd service — start automatisch bij login.

Om de service te stoppen:
```bash
launchctl unload ~/Library/LaunchAgents/com.deploystaton.server.plist
```
