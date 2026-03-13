# Deploy Station

Tool om zip-bestanden uit de Claude macOS app te uploaden en automatisch te deployen naar een lokaal project.

## Flow
1. Gebruiker downloadt zip uit Claude.ai chat
2. Opent Deploy Station in browser (http://mini.local:8080)
3. Kiest doelproject uit dropdown
4. Upload de zip via drag & drop
5. Server pakt zip uit in temp dir, kopieert naar project, doet git commit + push
6. Temp dir wordt opgeruimd

## Stack
- Single-file HTML frontend (geen build, geen frameworks)
- JSZip via CDN (alleen voor client-side preview)
- Python HTTP server (stdlib only, geen pip dependencies)

## Directory structuur
- public/index.html — de volledige UI, alles in een bestand
- server/app.py — Python backend (serve HTML + API endpoints)
- server/serve.sh — start server + registreert launchd service

## API endpoints
- GET / — serveert index.html
- GET /api/projects — lijst van ~/projects/ mappen
- POST /api/deploy — ontvangt zip + projectnaam, pakt uit, git commit+push

## Claude Code instructies
- Wijzig ALLEEN public/index.html voor UI aanpassingen
- Backend logica hoort in server/app.py
- Geen pip dependencies — alleen Python stdlib
- Geen externe JS dependencies behalve via CDN
- Geen build stap introduceren
- Wijzigingen zijn direct zichtbaar na browser refresh (herstart server bij backend wijzigingen)
