# Multi-stage Dockerfile for SlothChef 🍳🦥
# Stage 1: Build React 19 Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend Runtime
FROM python:3.11-slim
WORKDIR /app

# Install lightweight curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application & configuration
COPY backend/app/ ./backend/app/
COPY conftest.py ./

# Copy built frontend assets from Stage 1 into frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose Render port
EXPOSE 8000

ENV ENVIRONMENT=production
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV GEMMA_MODEL=gemma2:2b
ENV PYTHONPATH=/app/backend

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD sh -c "curl -f http://localhost:${PORT:-8000}/api/health || exit 1"

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
