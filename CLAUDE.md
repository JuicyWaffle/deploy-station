# Deploy Station

Tool om code-output uit Claude.ai chat om te zetten naar een zip met correcte directory structuur, klaar om uit te pakken in een project root.

## Doel
- Gebruiker plakt code + bestandspaden in de UI
- Tool genereert een zip met correcte directory structuur
- Zip uitpakken in project root, dan git push + ssh deploy

## Stack
- Single-file HTML (geen build stap, geen frameworks)
- JSZip via CDN voor zip generatie
- Python HTTP server om te serven op LAN

## Directory structuur
- public/index.html — de volledige tool, alles in één bestand
- server/serve.sh — start Python HTTP server + registreert launchd service

## Claude Code instructies
- Wijzig ALLEEN public/index.html voor UI aanpassingen
- Geen externe dependencies toevoegen behalve via CDN in de HTML
- Geen build stap introduceren
- Server logica hoort in serve.sh, niet in de HTML
- Na elke wijziging: git add -A && git commit -m "beschrijving" && git push
