#!/bin/bash

# RAG System Health Check Script
# Checks status of all system components

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

# Default values
STORAGE_BACKEND="${STORAGE_BACKEND:-local}"
PORT="${PORT:-8000}"
QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
NEO4J_HTTP_PORT="7474"

# Always use localhost for health checks (even if HOST is 0.0.0.0)
CHECK_HOST="localhost"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service health
check_service() {
    local service_name=$1
    local check_command=$2
    local timeout_seconds=${3:-5}

    printf "%-20s" "$service_name:"

    # Run command with timeout (cross-platform)
    if command -v timeout > /dev/null 2>&1; then
        # Linux/Mac - use timeout command
        if timeout $timeout_seconds bash -c "$check_command" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Healthy${NC}"
            return 0
        fi
    else
        # Windows/Git Bash - simple execution without timeout
        if eval "$check_command" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Healthy${NC}"
            return 0
        fi
    fi

    echo -e "${RED}✗ Unhealthy${NC}"
    return 1
}

echo "============================================"
echo "RAG System Health Check"
echo "============================================"
echo "Storage Backend: $STORAGE_BACKEND"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Check FastAPI Application
echo "============================================"
echo "FastAPI Application"
echo "============================================"
if check_service "FastAPI Server" "curl -f -s http://$CHECK_HOST:$PORT/api/v1/health"; then
    # Get detailed health info
    echo ""
    echo "Detailed Health Info:"
    curl -s "http://$CHECK_HOST:$PORT/api/v1/health" | python -m json.tool 2>/dev/null || echo "Failed to fetch health details"
fi
echo ""

# Check Database Services (if using qdrant_neo4j)
if [ "$STORAGE_BACKEND" = "qdrant_neo4j" ]; then
    echo "============================================"
    echo "Database Services"
    echo "============================================"

    # Check Docker
    check_service "Docker Daemon" "docker info"

    # Check Qdrant
    check_service "Qdrant" "curl -f -s $QDRANT_URL/healthz"

    # Check Neo4j
    check_service "Neo4j HTTP" "curl -f -s http://localhost:$NEO4J_HTTP_PORT"

    # Check PostgreSQL
    POSTGRES_USER="${POSTGRES_USER:-rag}"
    POSTGRES_DB="${POSTGRES_DB:-ragdb}"
    check_service "PostgreSQL" "docker-compose exec -T postgres pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"

    echo ""

    # Check Docker container status
    echo "============================================"
    echo "Docker Container Status"
    echo "============================================"
    docker-compose ps
    echo ""
else
    echo "============================================"
    echo "Storage Mode: Local"
    echo "============================================"
    echo "No database services to check"
    echo ""
fi

# Get storage statistics from API
echo "============================================"
echo "Storage Statistics"
echo "============================================"
if curl -f -s "http://$CHECK_HOST:$PORT/api/v1/health" > /dev/null 2>&1; then
    HEALTH_DATA=$(curl -s "http://$CHECK_HOST:$PORT/api/v1/health")

    # Parse storage info
    echo "Storage Backend: $(echo "$HEALTH_DATA" | python -c "import sys, json; data=json.load(sys.stdin); print(data.get('data', {}).get('storage_backend', 'unknown'))" 2>/dev/null || echo 'unknown')"

    # Try to get graph statistics
    echo ""
    echo "Knowledge Graph Statistics:"
    if curl -f -s "http://$CHECK_HOST:$PORT/api/v1/graph/stats" > /dev/null 2>&1; then
        curl -s "http://$CHECK_HOST:$PORT/api/v1/graph/stats" | python -m json.tool 2>/dev/null || echo "Failed to parse graph stats"
    else
        echo "Graph statistics endpoint not available"
    fi
else
    echo -e "${RED}Cannot fetch storage statistics - API is not responding${NC}"
fi

echo ""

# Check process status (cross-platform)
echo "============================================"
echo "Process Status"
echo "============================================"
if command -v pgrep > /dev/null 2>&1; then
    # Linux/Mac
    if pgrep -f "uvicorn app.main:app" > /dev/null 2>&1; then
        echo -e "${GREEN}FastAPI server process is running${NC}"
        echo "Process ID(s): $(pgrep -f 'uvicorn app.main:app' | tr '\n' ' ')"
    else
        echo -e "${RED}FastAPI server process is not running${NC}"
    fi
else
    # Windows/Git Bash
    PID=$(netstat -ano 2>/dev/null | grep ":$PORT" | grep "LISTENING" | awk '{print $5}' | head -1)
    if [ -n "$PID" ]; then
        echo -e "${GREEN}FastAPI server process is running${NC}"
        echo "Process ID: $PID"
    else
        echo -e "${RED}FastAPI server process is not running${NC}"
    fi
fi

echo ""

# Check log files
echo "============================================"
echo "Recent Logs"
echo "============================================"
LOG_FILE="$PROJECT_ROOT/logs/server.log"
if [ -f "$LOG_FILE" ]; then
    echo "Last 10 lines from server.log:"
    echo "---"
    tail -10 "$LOG_FILE"
else
    echo "No log file found at $LOG_FILE"
fi

echo ""
echo "============================================"
echo "Health Check Complete"
echo "============================================"
