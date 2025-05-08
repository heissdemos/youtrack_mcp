
FROM python:3.10-slim

WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Umgebungsvariablen für Docker-Betrieb setzen
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV MCP_LOG_LEVEL=DEBUG

# Pip-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt python-dotenv

# Quellcode kopieren
COPY *.py .
COPY *.md .
COPY bin/ ./bin/

# Port freigeben
EXPOSE 8000

# Health-Check-Script erstellen
RUN echo '#!/bin/bash\n\
curl -s http://localhost:8000/health | grep -q "ok" && exit 0 || exit 1\n\
' > /app/healthcheck.sh && chmod +x /app/healthcheck.sh

# Healthcheck hinzufügen, um Container-Monitoring zu ermöglichen
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD /app/healthcheck.sh

# Startskript für direkten Server-Start erstellen
RUN echo '#!/bin/bash\n\
echo "Starting YouTrack MCP Server with Docker optimizations..."\n\
# Docker-spezifische Umgebungsvariablen setzen\n\
export MCP_HOST=0.0.0.0\n\
export MCP_PORT=8000\n\
export YOUTRACK_URL=$YOUTRACK_URL\n\
export YOUTRACK_TOKEN=$YOUTRACK_TOKEN\n\
export YOUTRACK_READ_ONLY=$YOUTRACK_READ_ONLY\n\
\n\
# Server mit HTTP-Unterstützung starten - Using main.py which has SSE/HTTP support\n\
exec python main.py --transport sse --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Server starten
ENTRYPOINT ["/app/start.sh"]