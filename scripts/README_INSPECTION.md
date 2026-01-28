# Data Inspection Scripts

This directory contains inspection scripts for viewing stored data in Neo4j and Qdrant.

## Scripts

### inspect_neo4j.py

Inspects Neo4j knowledge graph data.

**Usage:**
```bash
python scripts/inspect_neo4j.py
```

**Features:**
- Displays database overview (node count, relationship count)
- Shows node statistics by label
- Shows relationship statistics by type
- Displays sample entities with properties
- Graceful error handling with helpful messages

**Configuration:**
Reads connection settings from environment variables (or .env file):
- `NEO4J_URI` (default: bolt://localhost:7687)
- `NEO4J_USER` (default: neo4j)
- `NEO4J_PASSWORD` (default: rag123456)
- `NEO4J_DATABASE` (default: neo4j)

### inspect_qdrant.py

Inspects Qdrant vector database data.

**Usage:**
```bash
python scripts/inspect_qdrant.py
```

**Features:**
- Lists all collections
- Displays collection statistics (vector count, size, distance metric)
- Shows sample points with payload
- Graceful error handling with helpful messages

**Configuration:**
Reads connection settings from environment variables (or .env file):
- `QDRANT_URL` (default: http://localhost:6333)
- `QDRANT_COLLECTION_NAME` (default: rag_collection)

## Requirements

Install required dependencies:
```bash
pip install neo4j qdrant-client python-dotenv
```

## Starting Services

If the scripts report connection errors, start the services:

```bash
# Start all services
docker-compose up -d

# Or start specific services
docker-compose up -d neo4j qdrant

# Or use the start script
./scripts/start.sh
```

## Verify Services

Check if services are running:
```bash
# Check Neo4j
docker ps | grep neo4j
curl http://localhost:7474

# Check Qdrant
docker ps | grep qdrant
curl http://localhost:6333/healthz
```

## Known Issues

### Neo4j Import Error (pandas/pyarrow)

If you encounter an error related to pandas/pyarrow version incompatibility:
```
AttributeError: module 'pyarrow' has no attribute '__version__'
```

**Solution:**
This is a known issue with certain pandas/pyarrow version combinations. Try:
```bash
pip install --upgrade pyarrow pandas
# or
pip install pyarrow==14.0.1 pandas==2.1.4
```

### Qdrant Connection Error (502 Bad Gateway)

If Python clients get 502 errors while curl works, this may be due to:
- System proxy configuration interfering with local requests
- Docker network issues

**Workaround:**
1. Check if Qdrant is actually accessible: `curl http://localhost:6333/healthz`
2. Restart Qdrant: `docker-compose restart qdrant`
3. Check Docker logs: `docker logs database-migration-qdrant-1`

## Empty Databases

If the databases are empty (no documents uploaded yet), the scripts will show:
```
[WARNING] Database is empty (no nodes found)
          Upload documents to populate the knowledge graph
```

This is expected behavior for a fresh installation. Upload documents via the API to populate the databases.

## Output Examples

### Neo4j Output (with data)
```
============================================================
  Database Overview
============================================================
  Total Nodes                    : 150
  Total Relationships            : 230
  Node Labels                    : 3
  Relationship Types             : 2

============================================================
  Node Statistics by Label
============================================================

  Label                                            Count
  ---------------------------------------- ---------------
  Entity                                               145
  Document                                               5

============================================================
  Relationship Statistics by Type
============================================================

  Type                                             Count
  ---------------------------------------- ---------------
  RELATED_TO                                           200
  FROM_DOCUMENT                                         30
```

### Qdrant Output (with data)
```
============================================================
  Qdrant Overview
============================================================
  Total Collections              : 1

============================================================
  All Collections
============================================================

  Collection Name                                Points
  ---------------------------------------- ---------------
  rag_collection                                    1,250

============================================================
  Collection: rag_collection
============================================================

  Configuration:
    Vector Size                  : 1024
    Distance Metric              : Cosine
    On-Disk Payload              : False

  Statistics:
    Status                       : green
    Points Count                 : 1,250
    Vectors Count                : 1,250
```

## Troubleshooting

1. **Import errors**: Ensure all required packages are installed
2. **Connection errors**: Verify services are running with Docker
3. **Empty output**: Upload documents to populate the databases
4. **Permission errors**: Run scripts from project root directory
5. **Encoding errors**: Scripts use ASCII-safe output (no emojis) for Windows compatibility
