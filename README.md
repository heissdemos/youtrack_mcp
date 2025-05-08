# YouTrack MCP Server

Ein Model Context Protocol (MCP) Server für YouTrack Integration mit Claude AI.

## Features

- Tickets suchen
- Detaillierte Ticket-Informationen abrufen
- Tickets aktualisieren (Status, Bearbeiter, etc.)
- Kommentare zu Tickets hinzufügen
- Standardisierte Schnittstelle über MCP
- Docker-Container für einfache Bereitstellung

## Anforderungen

- Docker
- Zugang zu YouTrack mit API-Token

## Schnellstart mit Docker

### 1. Kopiere die Beispiel-Umgebungsvariablen

```bash
cp .env.example .env
```

### 2. Konfiguriere die YouTrack-Verbindung

Bearbeite die `.env` Datei und aktualisiere die folgenden Werte:

```
YOUTRACK_URL=https://your-instance.youtrack.cloud
YOUTRACK_TOKEN=your-permanent-token
```

### 3. Server starten

Das einfachste ist, den Docker-Container mit dem mitgelieferten Skript zu starten:

```bash
./docker-run.sh
```

Alternativ kannst du auch manuell den Container bauen und starten:

```bash
docker build -t youtrack-mcp:latest .
docker run -d --name youtrack-mcp-server -p 8000:8000 --env-file ./.env youtrack-mcp:latest
```

#### Entwicklungsmodus

Für Entwicklungszwecke steht eine spezielle Dockerfile.dev zur Verfügung, die zusätzliche Tools und Funktionen für die Entwicklung enthält:

```bash
docker build -t youtrack-mcp:dev -f Dockerfile.dev .
docker run -d --name youtrack-mcp-dev -p 8000:8000 --env-file ./.env youtrack-mcp:dev
```

### 4. Server testen

```bash
# Health-Check
curl http://localhost:8000/health

# Server-Info abfragen
curl -s -X POST -H "Content-Type: application/json" -d '{"name": "server_info"}' http://localhost:8000/mcp
```

## Verfügbare Befehle

Der Server stellt die folgenden Befehle für die Arbeit mit YouTrack zur Verfügung:

- `server_info` - Server-Information abrufen
- `youtrack_search_issues` - Tickets suchen
- `youtrack_get_issue` - Detaillierte Informationen zu einem Ticket abrufen
- `youtrack_update_issue` - Ein Ticket aktualisieren
- `youtrack_add_comment` - Einen Kommentar zu einem Ticket hinzufügen

## Beispiele für die Verwendung

### Tickets suchen:

```bash
curl -s -X POST -H "Content-Type: application/json" -d '{
  "name": "youtrack_search_issues",
  "query": "project: YourProject",
  "top": 10
}' http://localhost:8000/mcp
```

### Ticket-Informationen abrufen:

```bash
curl -s -X POST -H "Content-Type: application/json" -d '{
  "name": "youtrack_get_issue",
  "issue_id": "YourProject-123"
}' http://localhost:8000/mcp
```

### Kommentar hinzufügen:

```bash
curl -s -X POST -H "Content-Type: application/json" -d '{
  "name": "youtrack_add_comment",
  "issue_id": "YourProject-123",
  "comment_text": "Neuer Kommentar zum Ticket"
}' http://localhost:8000/mcp
```

### Server-Informationen abrufen:

```bash
curl -s -X POST -H "Content-Type: application/json" -d '{
  "name": "server_info"
}' http://localhost:8000/mcp
```

## Architektur

Der YouTrack MCP Server besteht aus zwei Hauptkomponenten:

- `main.py` - MCP Server mit HTTP-Schnittstelle und Befehlsdefinitionen
- `youtrack_api.py` - Funktionen für die Interaktion mit der YouTrack API

## Integration mit Claude

Nachdem der Container erfolgreich gestartet wurde und funktioniert, musst du Claude mit dem MCP-Server verbinden. Führe dazu folgenden Befehl aus:

```bash
claude mcp add "YouTracker" http://localhost:8000/mcp -t sse
```

Dieser Befehl registriert den YouTrack MCP Server bei Claude und ermöglicht es Claude, direkt mit YouTrack zu kommunizieren.

## Weitere Dokumentation

Detaillierte Informationen zur Konfiguration und Verwendung des Docker-Containers findest du in [DOCKER.md](DOCKER.md).
