# Docker Infrastructure Setup

This document explains how to set up the V2.0 infrastructure services using Docker Compose.

## Services Overview

The docker-compose.yml file sets up the following services:

1. **Qdrant** (Port 6333) - Vector database for embeddings
2. **Redis** (Port 6379) - Cache and task queue
3. **PostgreSQL** (Port 5432) - Document metadata storage
4. **MinIO** (Ports 9000, 9001) - Object storage for uploaded files
5. **Celery Worker** - Background document processing

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of available RAM
- Ports 6333, 6379, 5432, 9000, 9001 available

## Quick Start

### 1. Start all services

```bash
docker-compose up -d
```

### 2. Verify services are running

```bash
docker-compose ps
```

All services should show status "Up".

### 3. Access service dashboards

- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **MinIO Console**: http://localhost:9001 (Login: minioadmin/minioadmin)
- **Redis**: Connect via CLI or GUI on localhost:6379

### 4. Update your .env file

Copy the V2.0 configuration from env.example:

```bash
# Qdrant
QDRANT_URL=http://localhost:6333

# Redis
REDIS_URI=redis://localhost:6379

# PostgreSQL
DATABASE_URL=postgresql://rag_user:rag_password@localhost:5432/rag_db

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

## Service Details

### Qdrant (Vector Database)

- **Storage**: `./data/qdrant_storage/`
- **API Port**: 6333 (HTTP), 6334 (gRPC)
- **Dashboard**: http://localhost:6333/dashboard

Qdrant stores all vector embeddings and enables fast similarity search.

### Redis (Cache & Queue)

- **Storage**: `./data/redis_data/`
- **Port**: 6379
- **Persistence**: AOF (append-only file)

Redis serves two purposes:
1. LLM response semantic cache
2. Celery task queue broker

### PostgreSQL (Metadata)

- **Storage**: `./data/postgres_data/`
- **Port**: 5432
- **Database**: rag_db
- **Credentials**: rag_user / rag_password

Stores structured document metadata (filename, status, timestamps, etc.).

### MinIO (Object Storage)

- **Storage**: `./data/minio_data/`
- **API Port**: 9000
- **Console Port**: 9001
- **Credentials**: minioadmin / minioadmin

Stores uploaded files and processing outputs. S3-compatible API.

### Celery Worker

Background worker for processing documents asynchronously. Connects to:
- Redis (for task queue)
- Qdrant (for vector storage)
- PostgreSQL (for metadata)
- MinIO (for file access)

## Common Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Stop services and remove data
```bash
docker-compose down -v
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f qdrant
docker-compose logs -f celery_worker
```

### Restart a service
```bash
docker-compose restart qdrant
```

## Data Persistence

All data is stored in `./data/` directory:

```
data/
├── qdrant_storage/     # Vector embeddings
├── redis_data/         # Cache data
├── postgres_data/      # Document metadata
└── minio_data/         # Uploaded files
```

To backup your data, simply backup the `./data/` directory.

## Troubleshooting

### Port conflicts

If any port is already in use, modify the port mappings in docker-compose.yml:

```yaml
ports:
  - "6333:6333"  # Change left number (host port)
```

### Service won't start

Check logs:
```bash
docker-compose logs [service_name]
```

### Reset everything

```bash
docker-compose down -v
rm -rf ./data/*
docker-compose up -d
```

## Production Deployment

For production:

1. Change default passwords in docker-compose.yml
2. Enable authentication for all services
3. Use external volumes for data persistence
4. Set up proper backup strategy
5. Use secrets management for credentials
6. Enable SSL/TLS for all connections

## Next Steps

After infrastructure is running:

1. Install Python dependencies: `pip install -r backend/requirements.txt`
2. Run database migrations (when ready)
3. Start backend: `cd backend && uvicorn app.main:app --reload`
4. Begin performance optimization implementation
