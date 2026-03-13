# Deploy Station

Upload zip-bestanden uit Claude.ai en deploy ze automatisch naar lokale projecten.

## Starten
```bash
bash ~/projects/deploy-station/server/serve.sh
```

Of direct:
```bash
python3 ~/projects/deploy-station/server/app.py
```

## Bereikbaar op
- http://localhost:8080
- http://mini.local:8080 (vanuit LAN)

## Gebruik
1. Open de URL in je browser
2. Kies een project uit de dropdown (toont mappen in ~/projects/)
3. Sleep een .zip bestand naar de upload zone
4. Klik "Deploy naar project"
5. De server pakt de zip uit, kopieert bestanden, en doet git commit + push

## Automatisch starten
serve.sh registreert een launchd service — start automatisch bij login.

Stoppen:
```bash
launchctl unload ~/Library/LaunchAgents/com.deploystation.server.plist
```
