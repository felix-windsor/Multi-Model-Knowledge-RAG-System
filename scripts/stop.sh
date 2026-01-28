#!/bin/bash

# RAG System Stop Script
# Stops FastAPI application and database services

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

echo "============================================"
echo "RAG System Shutdown"
echo "============================================"
echo "Storage Backend: $STORAGE_BACKEND"
echo ""

# Stop FastAPI application (cross-platform)
echo "Stopping FastAPI application..."
if command -v pkill > /dev/null 2>&1; then
    # Linux/Mac
    if pgrep -f "uvicorn app.main:app" > /dev/null 2>&1; then
        pkill -f "uvicorn app.main:app"
        echo "FastAPI application stopped"
        sleep 2
    else
        echo "FastAPI application is not running"
    fi
else
    # Windows/Git Bash - kill all python.exe processes
    # This is a simple but effective approach for development
    PORT="${PORT:-8000}"

    FOUND_PROCESS=false

    # Check if port is in use
    PORT_PID=$(netstat -ano 2>/dev/null | grep ":$PORT" | grep "LISTENING" | awk '{print $5}' | head -1)
    if [ -n "$PORT_PID" ] && [ "$PORT_PID" != "0" ]; then
        FOUND_PROCESS=true
    fi

    # Get all Python processes
    PYTHON_PIDS=$(tasklist //FI "IMAGENAME eq python.exe" //NH 2>/dev/null | awk '{print $2}' | grep -E '^[0-9]+$')

    if [ -n "$PYTHON_PIDS" ] && [ "$FOUND_PROCESS" = true ]; then
        echo "Stopping all Python processes (including uvicorn server)..."

        # Kill all Python processes with force and tree
        for pid in $PYTHON_PIDS; do
            taskkill //F //T //PID "$pid" > /dev/null 2>&1 || true
        done

        echo "FastAPI application stopped"
        sleep 2
    else
        echo "FastAPI application is not running"
    fi
fi

# Stop database services if using qdrant_neo4j backend
if [ "$STORAGE_BACKEND" = "qdrant_neo4j" ]; then
    echo ""
    echo "============================================"
    echo "Stopping Database Services"
    echo "============================================"

    cd "$PROJECT_ROOT"

    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        echo "WARNING: Docker is not running. Skipping database service shutdown."
    else
        # Stop services
        echo "Stopping Docker services..."
        docker-compose down

        echo "Database services stopped"
    fi
else
    echo ""
    echo "Using local storage mode - no database services to stop"
fi

echo ""
echo "============================================"
echo "RAG System Stopped Successfully!"
echo "============================================"
