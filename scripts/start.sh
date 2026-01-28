#!/bin/bash

# RAG System Start Script
# Supports both local and database storage modes

set -e

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

# Default to local storage if not set
STORAGE_BACKEND="${STORAGE_BACKEND:-local}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

echo "============================================"
echo "RAG System Startup"
echo "============================================"
echo "Storage Backend: $STORAGE_BACKEND"
echo "Project Root: $PROJECT_ROOT"
echo ""

# Function to wait for service health
wait_for_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    echo "Waiting for $service_name to be ready..."
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            echo "$service_name is ready!"
            return 0
        fi
        echo "  Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "ERROR: $service_name failed to become ready after $max_attempts attempts"
    return 1
}

# Start database services if using qdrant_neo4j backend
if [ "$STORAGE_BACKEND" = "qdrant_neo4j" ]; then
    echo "============================================"
    echo "Starting Database Services"
    echo "============================================"

    cd "$PROJECT_ROOT"

    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        echo "ERROR: Docker is not running. Please start Docker Desktop."
        exit 1
    fi

    # Start services
    echo "Starting Docker services..."
    docker-compose up -d

    echo ""
    echo "Waiting for services to be healthy..."
    echo ""

    # Wait for Qdrant
    QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
    if ! wait_for_service "Qdrant" "$QDRANT_URL/healthz"; then
        echo "Failed to start Qdrant. Check logs with: docker-compose logs qdrant"
        exit 1
    fi

    # Wait for Neo4j
    NEO4J_HTTP_PORT="${NEO4J_HTTP_PORT:-7474}"
    if ! wait_for_service "Neo4j" "http://localhost:$NEO4J_HTTP_PORT"; then
        echo "Failed to start Neo4j. Check logs with: docker-compose logs neo4j"
        exit 1
    fi

    # Wait for PostgreSQL
    if ! wait_for_service "PostgreSQL" "http://localhost:5432"; then
        # PostgreSQL doesn't have HTTP endpoint, so we check differently
        echo "Checking PostgreSQL with docker exec..."
        POSTGRES_USER="${POSTGRES_USER:-rag}"
        POSTGRES_DB="${POSTGRES_DB:-ragdb}"

        for i in {1..30}; do
            if docker-compose exec -T postgres pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; then
                echo "PostgreSQL is ready!"
                break
            fi
            if [ $i -eq 30 ]; then
                echo "ERROR: PostgreSQL failed to become ready"
                exit 1
            fi
            echo "  Attempt $i/30 - PostgreSQL not ready yet..."
            sleep 2
        done
    fi

    echo ""
    echo "All database services are ready!"
    echo ""
else
    echo "Using local storage mode - skipping database services"
    echo ""
fi

# Start FastAPI application
echo "============================================"
echo "Starting FastAPI Application"
echo "============================================"

cd "$PROJECT_ROOT/backend"

# Check if server is already running (cross-platform)
if command -v pgrep > /dev/null 2>&1; then
    # Linux/Mac
    if pgrep -f "uvicorn app.main:app" > /dev/null 2>&1; then
        echo "WARNING: Server is already running. Stop it first with scripts/stop.sh"
        exit 1
    fi
else
    # Windows/Git Bash - check if port is in use
    if netstat -ano 2>/dev/null | grep ":$PORT" | grep "LISTENING" > /dev/null 2>&1; then
        echo "WARNING: Port $PORT is already in use. Stop the server first with scripts/stop.sh"
        exit 1
    fi
fi

# Start server in background
echo "Starting uvicorn server..."
nohup python -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload > ../logs/server.log 2>&1 &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
echo ""

# Wait for server to be ready
echo "Waiting for FastAPI server to be ready..."
if ! wait_for_service "FastAPI" "http://localhost:$PORT/api/v1/health"; then
    echo "Failed to start FastAPI server. Check logs with: tail -f logs/server.log"
    exit 1
fi

echo ""
echo "============================================"
echo "RAG System Started Successfully!"
echo "============================================"
echo ""
echo "Access URLs:"
echo "  Frontend:    http://localhost:$PORT"
echo "  API Docs:    http://localhost:$PORT/docs"
echo "  Health:      http://localhost:$PORT/api/v1/health"
echo ""

if [ "$STORAGE_BACKEND" = "qdrant_neo4j" ]; then
    echo "Database UIs:"
    echo "  Qdrant:      http://localhost:6333/dashboard"
    echo "  Neo4j:       http://localhost:7474 (user: neo4j, pass: ${NEO4J_PASSWORD:-rag123456})"
    echo ""
fi

echo "Server logs:   tail -f $PROJECT_ROOT/logs/server.log"
echo ""
echo "To stop the system, run: bash scripts/stop.sh"
echo "============================================"
