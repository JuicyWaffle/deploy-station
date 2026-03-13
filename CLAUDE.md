# Deploy Station

## Doel

Deploy Station is een lokale single-file HTML tool waarmee je snel code-bestanden kunt bundelen tot een zip met de juiste directory structuur. De gegenereerde zip kun je uitpakken in een project root om bestanden te deployen.

## Directory Structuur

```
deploy-station/
├── CLAUDE.md          # Dit bestand — instructies voor Claude Code
├── README.md          # Gebruikersdocumentatie
├── public/
│   └── index.html     # De deploy tool (single-file, geen build)
└── server/
    └── serve.sh       # Start HTTP server + launchd service
```

## Regels voor Claude Code

- **Geen frameworks, geen build steps.** Alles blijft single-file HTML.
- `public/index.html` is het enige frontend-bestand. Alle CSS en JS staan inline.
- Enige toegestane externe dependency: JSZip via CDN.
- Wijzigingen aan `index.html` zijn direct zichtbaar na browser refresh.
- Voeg geen extra bestanden toe aan `public/` tenzij de gebruiker daar expliciet om vraagt.
- `server/serve.sh` beheert de Python HTTP server en launchd service. Pas dit alleen aan als er een probleem is met de server zelf.
- De server draait op poort 8080 en serveert de `public/` map.
