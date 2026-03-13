# Deploy Station

Lokale tool om code-bestanden te bundelen tot een zip met de juiste directory structuur.

## Server starten

```bash
cd ~/projects/deploy-station
bash server/serve.sh
```

Dit doet twee dingen:
1. Start een Python HTTP server op poort 8080 die `public/` serveert
2. Installeert een launchd service zodat de server automatisch start bij login

Na de eerste keer starten is de server altijd beschikbaar na het inloggen.

## Toegang

Open in je browser:

```
http://mini.local:8080
```

Of lokaal:

```
http://localhost:8080
```

## Gebruik

1. Klik op "Bestand toevoegen" om een nieuw bestand aan te maken
2. Vul het pad in (bijv. `src/components/Header.tsx`)
3. Plak of typ de code
4. Herhaal voor zoveel bestanden als nodig
5. Klik op "Download ZIP" — de zip bevat de exacte directory structuur

Pak de zip uit in je project root en de bestanden staan op de juiste plek.

## Server stoppen

```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.deploy-station.plist
```

## Server herstarten

```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.deploy-station.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.deploy-station.plist
```
