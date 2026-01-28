# Storage Backend Migration Guide

This guide provides comprehensive instructions for migrating between local file-based storage and database storage (Qdrant + Neo4j) in the Multi-Model Knowledge RAG System.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Understanding the Storage Backends](#understanding-the-storage-backends)
- [Migration Steps](#migration-steps)
  - [Migrating to Database Storage](#migrating-to-database-storage)
  - [Rolling Back to Local Storage](#rolling-back-to-local-storage)
- [Data Migration](#data-migration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Performance Tuning](#performance-tuning)
- [Best Practices](#best-practices)

## Overview

The Multi-Model Knowledge RAG System supports two storage backends:

1. **Local Storage** - File-based storage for development and single-instance deployments
2. **Database Storage** - Qdrant (vectors) + Neo4j (graph) for production and multi-instance deployments

**Critical Note:** Data is NOT automatically migrated between backends. When you switch backends, you start with an empty knowledge base and must re-upload documents.

## Prerequisites

### For Database Storage Migration

Before migrating to database storage, ensure you have:

1. **Docker and Docker Compose installed**
   ```bash
   # Check Docker version
   docker --version
   # Should output: Docker version 20.10.x or higher

   # Check Docker Compose version
   docker-compose --version
   # Should output: Docker Compose version 2.x or higher
   ```

2. **Sufficient system resources**
   - RAM: At least 4GB available (2GB for Qdrant, 2GB for Neo4j)
   - Disk: At least 10GB free space for database volumes
   - CPU: 2+ cores recommended

3. **Available ports**
   ```bash
   # Check if required ports are available (Windows)
   netstat -an | findstr "6333 7687 7474"

   # Check if required ports are available (Linux/Mac)
   netstat -an | grep -E "6333|7687|7474"

   # Expected: No output (ports are free)
   ```

   Required ports:
   - `6333` - Qdrant HTTP API
   - `7687` - Neo4j Bolt protocol
   - `7474` - Neo4j HTTP/Browser

4. **Backup of existing data** (if any)
   ```bash
   # Backup local storage data
   cp -r data/storage data/storage_backup_$(date +%Y%m%d)

   # Or on Windows
   xcopy data\storage data\storage_backup_%date% /E /I
   ```

### For Local Storage Migration

No special prerequisites needed - local storage is the default configuration.

## Understanding the Storage Backends

### Local Storage

**What it is:** File-based storage using LightRAG's native storage implementation.

**Storage locations:**
- Vectors: `data/storage/vdb_*.json`
- Graph: `data/storage/graph_*.graphml`
- Key-Value: `data/storage/kv_*.json`

**Advantages:**
- Zero configuration
- No external dependencies
- Fast for small datasets (<10,000 documents)
- Simple backup (copy files)
- Ideal for development

**Disadvantages:**
- No concurrent access
- Limited scalability
- No advanced querying
- File I/O bottleneck for large datasets

**Best for:** Development, testing, single-instance deployments, small datasets

### Database Storage

**What it is:** Production-grade storage using specialized databases.

**Components:**
- **Qdrant** - High-performance vector database for embeddings
- **Neo4j** - Graph database for entity relationships

**Advantages:**
- Concurrent access from multiple instances
- Horizontally scalable
- Advanced query capabilities
- Web UIs for data exploration
- Better performance for large datasets
- Production-ready with monitoring

**Disadvantages:**
- Requires Docker services
- More complex setup
- Higher resource usage

**Best for:** Production, multi-instance deployments, large datasets (>10,000 documents)

## Migration Steps

### Migrating to Database Storage

Follow these steps to migrate from local storage to database storage:

#### Step 1: Backup Current Data

Before starting, backup your current local storage:

```bash
# Backup local storage directory
cp -r data/storage data/storage_backup_$(date +%Y%m%d)

# On Windows
xcopy data\storage data\storage_backup_%date% /E /I
```

#### Step 2: Stop the Application

Stop the running FastAPI server:

```bash
# Press Ctrl+C in the terminal running uvicorn
# Or kill the process
pkill -f "uvicorn app.main:app"  # Linux/Mac
taskkill /F /IM python.exe       # Windows (if needed)
```

#### Step 3: Update Configuration

Edit your `.env` file in the project root:

```bash
# Change from:
STORAGE_BACKEND=local

# To:
STORAGE_BACKEND=qdrant_neo4j

# Add database connection settings (if not present):
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=rag_collection

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=rag123456
NEO4J_DATABASE=neo4j
```

**Important:** Do not modify other settings unless necessary. The LLM and API configurations remain unchanged.

#### Step 4: Start Database Services

Start Qdrant and Neo4j using Docker Compose:

```bash
# Start both services
docker-compose up -d qdrant neo4j

# Verify services are running
docker-compose ps

# Expected output:
# NAME          IMAGE                    STATUS         PORTS
# qdrant        qdrant/qdrant:latest     Up (healthy)   0.0.0.0:6333->6333/tcp
# neo4j         neo4j:latest             Up (healthy)   0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp
```

#### Step 5: Wait for Services to Be Ready

Database services need time to initialize:

```bash
# Check Qdrant health
curl http://localhost:6333/healthz
# Expected: OK

# Check Neo4j health (wait for "Running" status)
docker-compose logs neo4j | grep "Started."
# Expected: "Started."

# Usually takes 10-30 seconds for both services
```

**Alternative:** Use the health check script:

```bash
# Wait for services to be ready (bash/zsh)
until curl -sf http://localhost:6333/healthz > /dev/null; do
  echo "Waiting for Qdrant..."
  sleep 2
done
echo "Qdrant is ready!"

# For Windows PowerShell:
while (-not (Test-NetConnection localhost -Port 6333).TcpTestSucceeded) {
  Write-Host "Waiting for Qdrant..."
  Start-Sleep -Seconds 2
}
Write-Host "Qdrant is ready!"
```

#### Step 6: Start the Application

Start the FastAPI server:

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 7: Verify Migration

Check the application health endpoint:

```bash
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2026-01-28T12:00:00Z",
    "storage_backend": "qdrant_neo4j",
    "services": {
      "qdrant": "connected",
      "neo4j": "connected"
    }
  }
}
```

If you see `"storage_backend": "qdrant_neo4j"` and both services show `"connected"`, the migration is successful.

#### Step 8: Re-upload Documents

Since data is not automatically migrated, you must re-upload all documents:

**Option 1: Using the Web UI**
1. Open http://localhost:8000 in your browser
2. Navigate to the Upload section
3. Upload your documents one by one or in batch

**Option 2: Using the API**
```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf"

# Check processing status
curl http://localhost:8000/api/v1/documents/{doc_id}
```

**Option 3: Batch upload script**
```bash
# Create a simple batch upload script
for file in data/uploads/*.pdf; do
  echo "Uploading $file..."
  curl -X POST http://localhost:8000/api/v1/documents/upload \
    -F "file=@$file"
  sleep 2  # Wait between uploads
done
```

### Rolling Back to Local Storage

If you encounter issues or want to return to local storage:

#### Step 1: Stop the Application

```bash
# Press Ctrl+C in the terminal running uvicorn
```

#### Step 2: Update Configuration

Edit your `.env` file:

```bash
# Change from:
STORAGE_BACKEND=qdrant_neo4j

# To:
STORAGE_BACKEND=local

# Optional: Comment out database settings to avoid confusion
# QDRANT_URL=http://localhost:6333
# NEO4J_URI=bolt://localhost:7687
```

#### Step 3: Stop Database Services (Optional)

Free up system resources by stopping unused services:

```bash
# Stop database services
docker-compose stop qdrant neo4j

# Or completely remove them (data will be preserved in volumes)
docker-compose down
```

#### Step 4: Restore Backup (If Needed)

If you backed up your local storage before migration:

```bash
# Restore from backup
rm -rf data/storage
cp -r data/storage_backup_YYYYMMDD data/storage

# On Windows
rmdir /S /Q data\storage
xcopy data\storage_backup_YYYYMMDD data\storage /E /I
```

#### Step 5: Start the Application

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 6: Verify Rollback

```bash
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2026-01-28T12:00:00Z",
    "storage_backend": "local"
  }
}
```

## Data Migration

### Important Notes

1. **No Automatic Migration:** The system does not provide automatic data migration between backends. This is intentional to avoid data corruption and give you full control.

2. **Clean Start:** When you switch backends, you start with an empty knowledge base.

3. **Document Re-upload Required:** You must re-upload documents to populate the new backend.

### Manual Migration Options

If you need to preserve data when switching backends:

#### Option 1: Export and Re-import (Recommended)

1. **Before switching:** Export all documents and their metadata
2. **After switching:** Re-upload documents via API

This ensures proper processing with the new backend.

#### Option 2: Selective Migration

If you only need specific documents:

1. Identify critical documents
2. Switch backends
3. Re-upload only those critical documents
4. Gradually add other documents as needed

#### Option 3: Parallel Operation

Run both backends temporarily:

1. Keep old backend running on one instance
2. Start new backend on a different port
3. Gradually migrate traffic
4. Verify all functionality
5. Decommission old backend

### Data Backup Best Practices

1. **Before Migration:**
   ```bash
   # Backup local storage
   tar -czf storage_backup_$(date +%Y%m%d).tar.gz data/storage/

   # Backup uploads
   tar -czf uploads_backup_$(date +%Y%m%d).tar.gz data/uploads/
   ```

2. **Database Storage Backup:**
   ```bash
   # Backup Qdrant (creates a snapshot)
   curl -X POST http://localhost:6333/collections/rag_collection/snapshots

   # Backup Neo4j (using neo4j-admin)
   docker-compose exec neo4j neo4j-admin dump --database=neo4j --to=/backups/neo4j-backup.dump
   ```

3. **Restore Database Backup:**
   ```bash
   # Restore Qdrant snapshot
   curl -X PUT http://localhost:6333/collections/rag_collection/snapshots/upload \
     -H "Content-Type: application/octet-stream" \
     --data-binary @snapshot.tar

   # Restore Neo4j dump
   docker-compose exec neo4j neo4j-admin load --from=/backups/neo4j-backup.dump --database=neo4j --force
   ```

## Verification

### Post-Migration Verification Checklist

After completing migration, verify all functionality:

#### 1. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected: Status should be "healthy" with correct `storage_backend` value.

#### 2. Document Upload

```bash
# Upload a test document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test_document.pdf"

# Check document list
curl http://localhost:8000/api/v1/documents
```

Expected: Document should appear in the list with status "completed".

#### 3. Query Functionality

```bash
# Test query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?", "mode": "hybrid"}'
```

Expected: Should return relevant answer based on uploaded documents.

#### 4. Graph Functionality

```bash
# Get graph stats
curl http://localhost:8000/api/v1/graph/stats

# Get entities
curl http://localhost:8000/api/v1/graph/entities
```

Expected: Should return entities and relationships extracted from documents.

#### 5. Database Storage Verification (Database Backend Only)

**Qdrant:**
```bash
# Check collection info
curl http://localhost:6333/collections/rag_collection

# View in browser
open http://localhost:6333/dashboard  # Mac
start http://localhost:6333/dashboard # Windows
xdg-open http://localhost:6333/dashboard # Linux
```

**Neo4j:**
```bash
# View in browser (login: neo4j / rag123456)
open http://localhost:7474  # Mac
start http://localhost:7474 # Windows
xdg-open http://localhost:7474 # Linux

# Or use Cypher query
docker-compose exec neo4j cypher-shell -u neo4j -p rag123456 "MATCH (n:Entity) RETURN count(n)"
```

### Automated Verification Script

Create a verification script for comprehensive testing:

```bash
#!/bin/bash
# verify_migration.sh

echo "=== Migration Verification ==="

# 1. Health check
echo "1. Checking application health..."
health=$(curl -s http://localhost:8000/api/v1/health)
echo "$health" | python -m json.tool

# 2. Check storage backend
backend=$(echo "$health" | python -c "import sys, json; print(json.load(sys.stdin)['data']['storage_backend'])")
echo "Storage backend: $backend"

# 3. Test document list
echo "2. Checking document list..."
curl -s http://localhost:8000/api/v1/documents | python -m json.tool

# 4. Test graph stats
echo "3. Checking graph statistics..."
curl -s http://localhost:8000/api/v1/graph/stats | python -m json.tool

if [ "$backend" = "qdrant_neo4j" ]; then
  # 5. Check Qdrant
  echo "4. Checking Qdrant..."
  curl -s http://localhost:6333/collections/rag_collection | python -m json.tool

  # 6. Check Neo4j
  echo "5. Checking Neo4j..."
  docker-compose exec -T neo4j cypher-shell -u neo4j -p rag123456 "MATCH (n:Entity) RETURN count(n) as entity_count"
fi

echo "=== Verification Complete ==="
```

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Database Services Not Starting

**Symptoms:**
```bash
docker-compose ps
# Shows status as "Exited" or "Restarting"
```

**Solutions:**

1. **Check Docker logs:**
   ```bash
   docker-compose logs qdrant
   docker-compose logs neo4j
   ```

2. **Port conflicts:**
   ```bash
   # Check if ports are already in use
   netstat -an | grep -E "6333|7687|7474"

   # If ports are in use, stop the conflicting services or change ports in docker-compose.yml
   ```

3. **Insufficient memory:**
   ```bash
   # Check Docker memory allocation
   docker info | grep Memory

   # Increase Docker memory in Docker Desktop settings (recommend 4GB+)
   ```

4. **Full restart:**
   ```bash
   # Complete reset (WARNING: deletes all data)
   docker-compose down -v
   docker-compose up -d qdrant neo4j
   ```

#### Issue 2: Connection Errors

**Symptoms:**
```
Failed to connect to Qdrant: Connection refused
Failed to connect to Neo4j: Unable to retrieve routing information
```

**Solutions:**

1. **Wait for services to be ready:**
   ```bash
   # Services may still be initializing
   docker-compose logs -f qdrant neo4j
   # Wait until you see "Started" or "Ready" messages
   ```

2. **Check network connectivity:**
   ```bash
   # Test Qdrant
   curl http://localhost:6333/healthz

   # Test Neo4j
   curl http://localhost:7474
   ```

3. **Verify configuration:**
   ```bash
   # Check .env file
   grep QDRANT .env
   grep NEO4J .env

   # Ensure URLs match docker-compose.yml ports
   ```

4. **Check Docker network:**
   ```bash
   docker network inspect rag-network
   # Verify both containers are in the same network
   ```

5. **Firewall issues:**
   ```bash
   # Temporarily disable firewall to test (Linux)
   sudo ufw disable

   # Windows: Check Windows Firewall settings
   ```

#### Issue 3: Slow Query Performance

**Symptoms:**
- Queries take >5 seconds
- Timeouts occur
- High CPU/memory usage

**Solutions:**

1. **Check database performance:**
   ```bash
   # Qdrant stats
   curl http://localhost:6333/collections/rag_collection
   # Check "points_count" - if very high (>1M), may need optimization

   # Neo4j query plan
   docker-compose exec neo4j cypher-shell -u neo4j -p rag123456 \
     "EXPLAIN MATCH (n:Entity) RETURN n"
   ```

2. **Add indexes (Neo4j):**
   ```cypher
   # Create indexes for frequently queried properties
   CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name);
   CREATE INDEX entity_source IF NOT EXISTS FOR (e:Entity) ON (e.source_id);
   ```

3. **Optimize embedding settings:**
   ```bash
   # In .env file
   EMBEDDING_BATCH_NUM=32              # Increase batch size
   EMBEDDING_FUNC_MAX_ASYNC=16         # Increase concurrency
   EMBEDDING_CACHE_ENABLED=true        # Enable caching
   EMBEDDING_CACHE_THRESHOLD=0.95      # Cache similar embeddings
   ```

4. **Increase database resources:**
   ```yaml
   # In docker-compose.yml
   qdrant:
     environment:
       - QDRANT_MAX_SEGMENTS=10
     deploy:
       resources:
         limits:
           memory: 4G

   neo4j:
     environment:
       - NEO4J_dbms_memory_heap_max__size=2G
       - NEO4J_dbms_memory_pagecache_size=1G
   ```

#### Issue 4: Application Fails to Start

**Symptoms:**
```
Failed to create RAG instance
Storage backend initialization failed
```

**Solutions:**

1. **Check logs:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
   # Look for error messages
   ```

2. **Verify dependencies:**
   ```bash
   pip list | grep -E "qdrant|neo4j"
   # Should show: qdrant-client and neo4j

   # Reinstall if needed
   pip install -r requirements.txt
   ```

3. **Check configuration:**
   ```bash
   # Test config loading
   cd backend
   python -c "from app.config import settings; print(settings.STORAGE_BACKEND)"
   ```

4. **Test database connections manually:**
   ```python
   # test_connections.py
   from qdrant_client import QdrantClient
   from neo4j import GraphDatabase

   # Test Qdrant
   try:
       client = QdrantClient(url="http://localhost:6333")
       print("Qdrant:", client.get_collections())
   except Exception as e:
       print("Qdrant error:", e)

   # Test Neo4j
   try:
       driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "rag123456"))
       with driver.session() as session:
           result = session.run("RETURN 1")
           print("Neo4j:", result.single()[0])
       driver.close()
   except Exception as e:
       print("Neo4j error:", e)
   ```

#### Issue 5: Data Not Appearing After Upload

**Symptoms:**
- Document shows "completed" status
- But queries return no results
- Graph is empty

**Solutions:**

1. **Check document processing:**
   ```bash
   # Get document details
   curl http://localhost:8000/api/v1/documents/{doc_id}
   # Verify status is "completed" not "failed"
   ```

2. **Verify data in databases:**
   ```bash
   # Qdrant: Check point count
   curl http://localhost:6333/collections/rag_collection

   # Neo4j: Check entity count
   docker-compose exec neo4j cypher-shell -u neo4j -p rag123456 \
     "MATCH (n:Entity) RETURN count(n)"
   ```

3. **Check background task logs:**
   ```bash
   # Look for processing errors in application logs
   # Background tasks may have failed silently
   ```

4. **Re-upload with verbose logging:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
   # Then upload document and watch logs
   ```

#### Issue 6: Migration to Local Storage Fails

**Symptoms:**
- Application crashes when switching to local
- "Storage directory not found" error

**Solutions:**

1. **Create storage directory:**
   ```bash
   mkdir -p data/storage
   ```

2. **Check permissions:**
   ```bash
   # Ensure directory is writable
   chmod 755 data/storage  # Linux/Mac

   # On Windows, check folder properties -> Security
   ```

3. **Check STORAGE_DIR path:**
   ```bash
   # In .env
   STORAGE_DIR=../data/storage  # Relative to backend/
   # OR
   STORAGE_DIR=/absolute/path/to/data/storage
   ```

### Getting Help

If you continue to experience issues:

1. **Check logs:** Application logs and Docker logs contain detailed error messages
2. **Review configuration:** Double-check all `.env` settings
3. **Check documentation:** Review the main `CLAUDE.md` and API docs
4. **Test components:** Test database connections independently
5. **Community support:** Open an issue on GitHub with logs and configuration details

## Performance Tuning

### Database Storage Performance Optimization

#### Qdrant Optimization

1. **Collection Configuration:**
   ```python
   # Optimal settings for large datasets (modify in code if needed)
   from qdrant_client.models import VectorParams, Distance

   client.create_collection(
       collection_name="rag_collection",
       vectors_config=VectorParams(
           size=1024,
           distance=Distance.COSINE,
           on_disk=True  # Enable for datasets > 1M vectors
       ),
       optimizers_config={
           "indexing_threshold": 20000,  # Build index after 20k points
       }
   )
   ```

2. **Query Optimization:**
   ```bash
   # In .env - tune for your hardware
   EMBEDDING_BATCH_NUM=32              # Larger batches for faster embedding
   EMBEDDING_FUNC_MAX_ASYNC=16         # More concurrent requests
   ```

3. **Hardware Recommendations:**
   - CPU: 4+ cores for concurrent operations
   - RAM: 4GB minimum, 8GB+ for large datasets
   - Storage: SSD strongly recommended for index performance

#### Neo4j Optimization

1. **Memory Configuration:**
   ```yaml
   # In docker-compose.yml
   neo4j:
     environment:
       - NEO4J_dbms_memory_heap_max__size=2G           # JVM heap
       - NEO4J_dbms_memory_pagecache_size=1G           # Page cache
       - NEO4J_dbms_tx__log_rotation_retention__policy=false
   ```

2. **Create Indexes:**
   ```cypher
   // In Neo4j Browser (http://localhost:7474)

   // Index on entity names for faster lookups
   CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name);

   // Index on source documents
   CREATE INDEX entity_source IF NOT EXISTS FOR (e:Entity) ON (e.source_id);

   // Index on relationship types
   CREATE INDEX relationship_type IF NOT EXISTS FOR ()-[r:RELATIONSHIP]-() ON (r.type);

   // View all indexes
   SHOW INDEXES;
   ```

3. **Query Performance:**
   ```cypher
   // Use query profiling to identify bottlenecks
   PROFILE MATCH (e:Entity)-[r:RELATIONSHIP]->(target)
   WHERE e.name = "Entity Name"
   RETURN e, r, target;

   // Optimize by limiting results
   MATCH (e:Entity)-[r:RELATIONSHIP]->(target)
   RETURN e, r, target
   LIMIT 100;
   ```

#### Application-Level Optimization

1. **Embedding Caching:**
   ```bash
   # In .env
   EMBEDDING_CACHE_ENABLED=true
   EMBEDDING_CACHE_THRESHOLD=0.95  # Cache similarity threshold
   ```

2. **Batch Processing:**
   ```bash
   # Process documents in batches to reduce load
   # Upload 10-20 documents at a time, wait for completion
   ```

3. **Connection Pooling:**
   The application automatically manages connection pools. Adjust if needed:
   ```python
   # In backend/app/config.py (for advanced users)
   QDRANT_TIMEOUT = 60  # Increase for slow networks
   NEO4J_MAX_CONNECTION_LIFETIME = 3600
   ```

### Monitoring Performance

#### Qdrant Metrics

```bash
# Collection statistics
curl http://localhost:6333/collections/rag_collection | python -m json.tool

# Key metrics:
# - points_count: Total vectors stored
# - segments_count: Number of index segments
# - status: Collection health
```

#### Neo4j Metrics

```cypher
// In Neo4j Browser

// Count all nodes and relationships
MATCH (n) RETURN count(n) as total_nodes;
MATCH ()-[r]->() RETURN count(r) as total_relationships;

// Database size
CALL db.stats.retrieve('GRAPH COUNTS');

// Query performance
CALL dbms.listQueries();
```

#### Application Metrics

```bash
# Health endpoint includes performance info
curl http://localhost:8000/api/v1/health | python -m json.tool

# Graph stats endpoint
curl http://localhost:8000/api/v1/graph/stats | python -m json.tool
```

### Benchmark Results

Typical performance characteristics:

| Operation | Local Storage | Database Storage |
|-----------|---------------|------------------|
| Document Upload (1MB PDF) | 5-10s | 8-15s |
| Query (hybrid mode) | 2-5s | 1-3s |
| Graph Export (1000 nodes) | 1-2s | 0.5-1s |
| Concurrent Queries (10) | Serial | Parallel |

Database storage is slower for uploads but faster for queries, especially with concurrent access.

## Best Practices

### 1. Development Workflow

**Recommendation:** Use local storage for development, database storage for staging/production.

```bash
# Development: .env.development
STORAGE_BACKEND=local
STORAGE_DIR=../data/storage_dev

# Production: .env.production
STORAGE_BACKEND=qdrant_neo4j
QDRANT_URL=http://qdrant:6333
NEO4J_URI=bolt://neo4j:7687
```

### 2. Backup Strategy

**Daily Backups:**
```bash
# Automate with cron (Linux/Mac)
0 2 * * * /path/to/backup_script.sh

# backup_script.sh:
#!/bin/bash
DATE=$(date +%Y%m%d)
docker-compose exec -T neo4j neo4j-admin dump --database=neo4j --to=/backups/neo4j-$DATE.dump
curl -X POST http://localhost:6333/collections/rag_collection/snapshots
```

**Pre-Migration Backup:**
Always backup before switching backends.

### 3. Capacity Planning

**Local Storage:**
- Suitable for: <10,000 documents, <1GB total data
- Beyond this: Consider database storage

**Database Storage:**
- Plan for: 100MB RAM per 10,000 vectors
- Disk space: 2-3x the size of uploaded documents
- Network: Low latency between app and databases

### 4. Security Considerations

**Database Credentials:**
```bash
# Never use default credentials in production
NEO4J_PASSWORD=use_strong_password_here  # Change this!

# Use environment-specific .env files
.env.development
.env.staging
.env.production

# Add to .gitignore
.env*
!env.example
```

**Network Security:**
```yaml
# In docker-compose.yml for production
services:
  qdrant:
    environment:
      - QDRANT_API_KEY=${QDRANT_API_KEY}  # Enable API key auth
  neo4j:
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
```

### 5. Monitoring and Alerting

**Health Checks:**
```bash
# Set up monitoring with cron
*/5 * * * * curl -f http://localhost:8000/api/v1/health || echo "Service down!" | mail -s "Alert" admin@example.com
```

**Database Monitoring:**
- Qdrant: Monitor collection size, query latency
- Neo4j: Monitor query performance, connection count
- System: Monitor CPU, RAM, disk I/O

### 6. Scaling Strategies

**Vertical Scaling:**
```yaml
# Increase resources in docker-compose.yml
services:
  qdrant:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

**Horizontal Scaling:**
- Qdrant: Supports clustering (requires Qdrant Cloud or manual setup)
- Neo4j: Use Neo4j clustering (requires Enterprise Edition)
- Application: Run multiple instances behind a load balancer

### 7. Maintenance Windows

**Recommended Schedule:**
- Weekly: Review logs, check disk space
- Monthly: Optimize databases, update indexes
- Quarterly: Full backup, capacity review

**Maintenance Tasks:**
```bash
# Qdrant optimization
curl -X POST http://localhost:6333/collections/rag_collection/optimize

# Neo4j maintenance (during low traffic)
docker-compose exec neo4j cypher-shell -u neo4j -p rag123456 "CALL db.checkpoint();"
```

### 8. Testing Before Production

**Pre-Production Checklist:**
- [ ] Test document upload with representative samples
- [ ] Verify query performance with expected load
- [ ] Test failover scenarios (service restart)
- [ ] Validate backup and restore procedures
- [ ] Perform load testing (use tools like Apache Bench)
- [ ] Review and tune database configurations
- [ ] Set up monitoring and alerting
- [ ] Document any custom configurations

## Conclusion

This guide has covered:
- Understanding both storage backends
- Step-by-step migration procedures
- Verification and validation steps
- Common troubleshooting scenarios
- Performance optimization strategies
- Best practices for production deployments

**Key Takeaways:**
1. Data is NOT automatically migrated - plan accordingly
2. Database storage requires Docker but provides better scalability
3. Always backup before migration
4. Test thoroughly after migration
5. Monitor performance and optimize as needed

For additional help, refer to:
- Main documentation: `CLAUDE.md`
- API documentation: http://localhost:8000/docs
- GitHub issues: [Project repository]

**Questions or Issues?** Open an issue on GitHub with:
- Your current configuration (.env with secrets redacted)
- Logs from application and Docker services
- Steps you've already tried
- Expected vs actual behavior
