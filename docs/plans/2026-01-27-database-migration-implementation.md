# Database Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate storage from local files to PostgreSQL + Qdrant + Neo4j with configuration-based backend switching.

**Architecture:** Add storage abstraction layer with interface classes, implement local and database backends, modify existing services to use the abstraction. LightRAG vector/graph storage uses native plugin mechanism.

**Tech Stack:** PostgreSQL 16, Qdrant, Neo4j 5, asyncpg, Docker Compose, Pydantic

---

## Phase 1: Infrastructure Setup

### Task 1.1: Create Docker Compose Configuration

**Files:**
- Create: `docker-compose.yml`
- Create: `docker-compose.prod.yml`

**Step 1: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-rag}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-rag123}
      POSTGRES_DB: ${POSTGRES_DB:-ragdb}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rag -d ragdb"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - rag-network

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
      - "6334:6334"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/healthz"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - rag-network

  neo4j:
    image: neo4j:5-community
    environment:
      NEO4J_AUTH: ${NEO4J_USER:-neo4j}/${NEO4J_PASSWORD:-rag123456}
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
    ports:
      - "7474:7474"
      - "7687:7687"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7474"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    networks:
      - rag-network

networks:
  rag-network:
    driver: bridge

volumes:
  postgres_data:
  qdrant_data:
  neo4j_data:
```

**Step 2: Create docker-compose.prod.yml**

```yaml
version: '3.8'

services:
  postgres:
    ports: []

  qdrant:
    ports: []

  neo4j:
    ports: []
```

**Step 3: Commit**

```bash
git add docker-compose.yml docker-compose.prod.yml
git commit -m "feat: add Docker Compose for database services"
```

---

### Task 1.2: Create Database Init Script

**Files:**
- Create: `scripts/init.sql`

**Step 1: Create scripts directory and init.sql**

```sql
-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    file_size BIGINT,
    mime_type VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    last_error TEXT,
    result JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Webhooks table
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    callback_url VARCHAR(500) NOT NULL,
    event_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    last_error TEXT,
    next_retry_at TIMESTAMP,
    delivered_at TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_document_id ON tasks(document_id);
CREATE INDEX IF NOT EXISTS idx_webhooks_status ON webhooks(status);
CREATE INDEX IF NOT EXISTS idx_webhooks_next_retry ON webhooks(next_retry_at)
    WHERE status = 'pending';
```

**Step 2: Commit**

```bash
git add scripts/init.sql
git commit -m "feat: add PostgreSQL init script with tables and indexes"
```

---

### Task 1.3: Update Environment Configuration

**Files:**
- Modify: `env.example`
- Modify: `backend/app/config.py`

**Step 1: Add database config to env.example**

Append to `env.example`:

```bash
# ============================================
# Storage Backend Configuration
# ============================================
STORAGE_BACKEND=local  # local | database

# ============================================
# PostgreSQL Configuration (when STORAGE_BACKEND=database)
# ============================================
POSTGRES_USER=rag
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=ragdb
DATABASE_URL=postgresql://rag:your-secure-password@localhost:5432/ragdb

# ============================================
# Qdrant Configuration (when STORAGE_BACKEND=database)
# ============================================
QDRANT_HOST=localhost
QDRANT_PORT=6333

# ============================================
# Neo4j Configuration (when STORAGE_BACKEND=database)
# ============================================
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-secure-password
NEO4J_DATABASE=neo4j
```

**Step 2: Add config fields to backend/app/config.py**

Add after line 67 (after `embedding_cache_threshold`):

```python
    # ============================================
    # Storage Backend Configuration
    # ============================================
    storage_backend: str = "local"  # local | database

    # PostgreSQL
    postgres_user: str = "rag"
    postgres_password: str = "rag123"
    postgres_db: str = "ragdb"
    database_url: Optional[str] = None

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "rag123456"
    neo4j_database: str = "neo4j"
```

**Step 3: Commit**

```bash
git add env.example backend/app/config.py
git commit -m "feat: add storage backend configuration options"
```

---

### Task 1.4: Verify Infrastructure

**Step 1: Start database services**

```bash
docker-compose up -d postgres qdrant neo4j
```

**Step 2: Verify PostgreSQL**

```bash
docker-compose exec postgres psql -U rag -d ragdb -c "SELECT 1"
```

Expected: Returns `1`

**Step 3: Verify Qdrant**

```bash
curl http://localhost:6333/healthz
```

Expected: Returns `ok` or similar

**Step 4: Verify Neo4j**

```bash
curl http://localhost:7474
```

Expected: Returns HTML or JSON response

**Step 5: Verify tables created**

```bash
docker-compose exec postgres psql -U rag -d ragdb -c "\dt"
```

Expected: Lists documents, tasks, webhooks tables

---

## Phase 2: Storage Abstraction Layer

### Task 2.1: Create Storage Models

**Files:**
- Create: `backend/app/storage/__init__.py`
- Create: `backend/app/storage/models.py`

**Step 1: Create storage directory**

```bash
mkdir -p backend/app/storage
```

**Step 2: Create models.py with Pydantic models**

```python
"""Storage layer data models"""
from datetime import datetime
from typing import Optional, Any, Dict
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WebhookStatus(str, Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"


class Document(BaseModel):
    id: UUID
    filename: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    status: DocumentStatus = DocumentStatus.PENDING
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Task(BaseModel):
    id: UUID
    document_id: UUID
    task_type: str
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    retry_count: int = 0
    max_retries: int = 3
    last_error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Webhook(BaseModel):
    id: UUID
    document_id: UUID
    callback_url: str
    event_type: Optional[str] = None
    status: WebhookStatus = WebhookStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    last_error: Optional[str] = None
    next_retry_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```

**Step 3: Create __init__.py**

```python
"""Storage layer package"""
from .models import Document, Task, Webhook, DocumentStatus, TaskStatus, WebhookStatus

__all__ = [
    "Document",
    "Task",
    "Webhook",
    "DocumentStatus",
    "TaskStatus",
    "WebhookStatus",
]
```

**Step 4: Commit**

```bash
git add backend/app/storage/
git commit -m "feat: add storage layer data models"
```

---

### Task 2.2: Create Abstract Storage Interfaces

**Files:**
- Create: `backend/app/storage/base.py`

**Step 1: Create base.py with abstract interfaces**

```python
"""Abstract storage interfaces"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

from .models import Document, Task, Webhook


class DocumentStorage(ABC):
    """Document metadata storage interface"""

    @abstractmethod
    async def create(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str
    ) -> Document:
        """Create a new document record"""
        pass

    @abstractmethod
    async def get(self, doc_id: UUID) -> Optional[Document]:
        """Get document by ID"""
        pass

    @abstractmethod
    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Document]:
        """List documents with optional filtering"""
        pass

    @abstractmethod
    async def update_status(
        self,
        doc_id: UUID,
        status: str,
        error_message: Optional[str] = None
    ) -> bool:
        """Update document status"""
        pass

    @abstractmethod
    async def delete(self, doc_id: UUID) -> bool:
        """Delete document and cascade to related records"""
        pass


class TaskStorage(ABC):
    """Task storage interface"""

    @abstractmethod
    async def create(self, document_id: UUID, task_type: str) -> Task:
        """Create a new task"""
        pass

    @abstractmethod
    async def get(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        pass

    @abstractmethod
    async def get_by_document(self, document_id: UUID) -> List[Task]:
        """Get all tasks for a document"""
        pass

    @abstractmethod
    async def list_pending(self, limit: int = 10) -> List[Task]:
        """Get pending tasks for processing"""
        pass

    @abstractmethod
    async def start(self, task_id: UUID) -> bool:
        """Mark task as started"""
        pass

    @abstractmethod
    async def update_progress(self, task_id: UUID, progress: int) -> bool:
        """Update task progress (0-100)"""
        pass

    @abstractmethod
    async def complete(self, task_id: UUID, result: Optional[Any] = None) -> bool:
        """Mark task as completed"""
        pass

    @abstractmethod
    async def fail(self, task_id: UUID, error: str) -> bool:
        """Mark task as failed, handle retry logic"""
        pass

    @abstractmethod
    async def cancel(self, task_id: UUID) -> bool:
        """Cancel a pending or processing task"""
        pass


class WebhookStorage(ABC):
    """Webhook storage interface"""

    @abstractmethod
    async def create(
        self,
        document_id: UUID,
        callback_url: str,
        event_type: str
    ) -> Webhook:
        """Create a new webhook"""
        pass

    @abstractmethod
    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        """Get webhook by ID"""
        pass

    @abstractmethod
    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        """Get all webhooks for a document"""
        pass

    @abstractmethod
    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        """Get pending webhooks (including due retries)"""
        pass

    @abstractmethod
    async def mark_delivered(self, webhook_id: UUID) -> bool:
        """Mark webhook as successfully delivered"""
        pass

    @abstractmethod
    async def mark_failed(
        self,
        webhook_id: UUID,
        error: str,
        retry_after: Optional[datetime] = None
    ) -> bool:
        """Mark webhook as failed, schedule retry"""
        pass


class StorageManager:
    """Unified storage manager"""

    def __init__(
        self,
        documents: DocumentStorage,
        tasks: TaskStorage,
        webhooks: WebhookStorage
    ):
        self.documents = documents
        self.tasks = tasks
        self.webhooks = webhooks
```

**Step 2: Update __init__.py**

```python
"""Storage layer package"""
from .models import Document, Task, Webhook, DocumentStatus, TaskStatus, WebhookStatus
from .base import DocumentStorage, TaskStorage, WebhookStorage, StorageManager

__all__ = [
    "Document",
    "Task",
    "Webhook",
    "DocumentStatus",
    "TaskStatus",
    "WebhookStatus",
    "DocumentStorage",
    "TaskStorage",
    "WebhookStorage",
    "StorageManager",
]
```

**Step 3: Commit**

```bash
git add backend/app/storage/
git commit -m "feat: add abstract storage interfaces"
```

---

### Task 2.3: Implement Local Document Storage

**Files:**
- Create: `backend/app/storage/local/__init__.py`
- Create: `backend/app/storage/local/document.py`

**Step 1: Create local storage directory**

```bash
mkdir -p backend/app/storage/local
```

**Step 2: Create document.py**

```python
"""Local file-based document storage"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from ..base import DocumentStorage
from ..models import Document, DocumentStatus


class LocalDocumentStorage(DocumentStorage):
    """Local JSON file-based document storage"""

    def __init__(self, storage_dir: str = "data/storage"):
        self.storage_dir = Path(storage_dir)
        self.documents_file = self.storage_dir / "documents.json"
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Ensure storage directory and file exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.documents_file.exists():
            self._save_documents({})

    def _load_documents(self) -> dict:
        """Load documents from JSON file"""
        try:
            with open(self.documents_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_documents(self, documents: dict):
        """Save documents to JSON file"""
        with open(self.documents_file, "w", encoding="utf-8") as f:
            json.dump(documents, f, indent=2, default=str)

    async def create(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str
    ) -> Document:
        """Create a new document record"""
        documents = self._load_documents()

        doc_id = uuid.uuid4()
        now = datetime.now()

        doc_data = {
            "id": str(doc_id),
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "mime_type": mime_type,
            "status": DocumentStatus.PENDING.value,
            "error_message": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

        documents[str(doc_id)] = doc_data
        self._save_documents(documents)

        return Document(
            id=doc_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            status=DocumentStatus.PENDING,
            created_at=now,
            updated_at=now
        )

    async def get(self, doc_id: UUID) -> Optional[Document]:
        """Get document by ID"""
        documents = self._load_documents()
        doc_data = documents.get(str(doc_id))

        if not doc_data:
            return None

        return Document(
            id=UUID(doc_data["id"]),
            filename=doc_data["filename"],
            file_path=doc_data.get("file_path"),
            file_size=doc_data.get("file_size"),
            mime_type=doc_data.get("mime_type"),
            status=DocumentStatus(doc_data["status"]),
            error_message=doc_data.get("error_message"),
            created_at=datetime.fromisoformat(doc_data["created_at"]),
            updated_at=datetime.fromisoformat(doc_data["updated_at"])
        )

    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Document]:
        """List documents with optional filtering"""
        documents = self._load_documents()

        result = []
        for doc_data in documents.values():
            if status and doc_data["status"] != status:
                continue

            result.append(Document(
                id=UUID(doc_data["id"]),
                filename=doc_data["filename"],
                file_path=doc_data.get("file_path"),
                file_size=doc_data.get("file_size"),
                mime_type=doc_data.get("mime_type"),
                status=DocumentStatus(doc_data["status"]),
                error_message=doc_data.get("error_message"),
                created_at=datetime.fromisoformat(doc_data["created_at"]),
                updated_at=datetime.fromisoformat(doc_data["updated_at"])
            ))

        # Sort by created_at descending
        result.sort(key=lambda x: x.created_at, reverse=True)

        return result[offset:offset + limit]

    async def update_status(
        self,
        doc_id: UUID,
        status: str,
        error_message: Optional[str] = None
    ) -> bool:
        """Update document status"""
        documents = self._load_documents()
        doc_key = str(doc_id)

        if doc_key not in documents:
            return False

        documents[doc_key]["status"] = status
        documents[doc_key]["updated_at"] = datetime.now().isoformat()

        if error_message is not None:
            documents[doc_key]["error_message"] = error_message

        self._save_documents(documents)
        return True

    async def delete(self, doc_id: UUID) -> bool:
        """Delete document"""
        documents = self._load_documents()
        doc_key = str(doc_id)

        if doc_key not in documents:
            return False

        del documents[doc_key]
        self._save_documents(documents)
        return True
```

**Step 3: Create __init__.py**

```python
"""Local storage implementations"""
from .document import LocalDocumentStorage

__all__ = ["LocalDocumentStorage"]
```

**Step 4: Commit**

```bash
git add backend/app/storage/local/
git commit -m "feat: implement local document storage"
```

---

### Task 2.4: Implement Local Task Storage

**Files:**
- Create: `backend/app/storage/local/task.py`
- Modify: `backend/app/storage/local/__init__.py`

**Step 1: Create task.py**

```python
"""Local file-based task storage"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Any
from uuid import UUID

from ..base import TaskStorage
from ..models import Task, TaskStatus


class LocalTaskStorage(TaskStorage):
    """Local JSON file-based task storage"""

    def __init__(self, storage_dir: str = "data/storage"):
        self.storage_dir = Path(storage_dir)
        self.tasks_file = self.storage_dir / "tasks.json"
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Ensure storage directory and file exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.tasks_file.exists():
            self._save_tasks({})

    def _load_tasks(self) -> dict:
        """Load tasks from JSON file"""
        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_tasks(self, tasks: dict):
        """Save tasks to JSON file"""
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, default=str)

    def _task_from_dict(self, data: dict) -> Task:
        """Convert dict to Task model"""
        return Task(
            id=UUID(data["id"]),
            document_id=UUID(data["document_id"]),
            task_type=data["task_type"],
            status=TaskStatus(data["status"]),
            progress=data.get("progress", 0),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            last_error=data.get("last_error"),
            result=data.get("result"),
            created_at=datetime.fromisoformat(data["created_at"]),
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        )

    async def create(self, document_id: UUID, task_type: str) -> Task:
        """Create a new task"""
        tasks = self._load_tasks()

        task_id = uuid.uuid4()
        now = datetime.now()

        task_data = {
            "id": str(task_id),
            "document_id": str(document_id),
            "task_type": task_type,
            "status": TaskStatus.PENDING.value,
            "progress": 0,
            "retry_count": 0,
            "max_retries": 3,
            "last_error": None,
            "result": None,
            "created_at": now.isoformat(),
            "started_at": None,
            "completed_at": None
        }

        tasks[str(task_id)] = task_data
        self._save_tasks(tasks)

        return self._task_from_dict(task_data)

    async def get(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        tasks = self._load_tasks()
        task_data = tasks.get(str(task_id))

        if not task_data:
            return None

        return self._task_from_dict(task_data)

    async def get_by_document(self, document_id: UUID) -> List[Task]:
        """Get all tasks for a document"""
        tasks = self._load_tasks()
        doc_id_str = str(document_id)

        result = [
            self._task_from_dict(data)
            for data in tasks.values()
            if data["document_id"] == doc_id_str
        ]

        result.sort(key=lambda x: x.created_at, reverse=True)
        return result

    async def list_pending(self, limit: int = 10) -> List[Task]:
        """Get pending tasks for processing"""
        tasks = self._load_tasks()

        result = [
            self._task_from_dict(data)
            for data in tasks.values()
            if data["status"] == TaskStatus.PENDING.value
        ]

        result.sort(key=lambda x: x.created_at)
        return result[:limit]

    async def start(self, task_id: UUID) -> bool:
        """Mark task as started"""
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        tasks[task_key]["status"] = TaskStatus.PROCESSING.value
        tasks[task_key]["started_at"] = datetime.now().isoformat()

        self._save_tasks(tasks)
        return True

    async def update_progress(self, task_id: UUID, progress: int) -> bool:
        """Update task progress (0-100)"""
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        tasks[task_key]["progress"] = max(0, min(100, progress))

        self._save_tasks(tasks)
        return True

    async def complete(self, task_id: UUID, result: Optional[Any] = None) -> bool:
        """Mark task as completed"""
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        now = datetime.now()
        tasks[task_key]["status"] = TaskStatus.COMPLETED.value
        tasks[task_key]["progress"] = 100
        tasks[task_key]["completed_at"] = now.isoformat()

        if result is not None:
            tasks[task_key]["result"] = result

        self._save_tasks(tasks)
        return True

    async def fail(self, task_id: UUID, error: str) -> bool:
        """Mark task as failed, handle retry logic"""
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        task = tasks[task_key]
        task["retry_count"] = task.get("retry_count", 0) + 1
        task["last_error"] = error

        # Check if we should retry
        if task["retry_count"] < task.get("max_retries", 3):
            task["status"] = TaskStatus.PENDING.value
        else:
            task["status"] = TaskStatus.FAILED.value
            task["completed_at"] = datetime.now().isoformat()

        self._save_tasks(tasks)
        return True

    async def cancel(self, task_id: UUID) -> bool:
        """Cancel a pending or processing task"""
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        task = tasks[task_key]

        # Can only cancel pending or processing tasks
        if task["status"] not in [TaskStatus.PENDING.value, TaskStatus.PROCESSING.value]:
            return False

        task["status"] = TaskStatus.CANCELLED.value
        task["completed_at"] = datetime.now().isoformat()

        self._save_tasks(tasks)
        return True
```

**Step 2: Update __init__.py**

```python
"""Local storage implementations"""
from .document import LocalDocumentStorage
from .task import LocalTaskStorage

__all__ = ["LocalDocumentStorage", "LocalTaskStorage"]
```

**Step 3: Commit**

```bash
git add backend/app/storage/local/
git commit -m "feat: implement local task storage"
```

---

### Task 2.5: Implement Local Webhook Storage

**Files:**
- Create: `backend/app/storage/local/webhook.py`
- Modify: `backend/app/storage/local/__init__.py`

**Step 1: Create webhook.py**

```python
"""Local file-based webhook storage"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from ..base import WebhookStorage
from ..models import Webhook, WebhookStatus


class LocalWebhookStorage(WebhookStorage):
    """Local JSON file-based webhook storage"""

    def __init__(self, storage_dir: str = "data/storage"):
        self.storage_dir = Path(storage_dir)
        self.webhooks_file = self.storage_dir / "webhooks.json"
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Ensure storage directory and file exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.webhooks_file.exists():
            self._save_webhooks({})

    def _load_webhooks(self) -> dict:
        """Load webhooks from JSON file"""
        try:
            with open(self.webhooks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_webhooks(self, webhooks: dict):
        """Save webhooks to JSON file"""
        with open(self.webhooks_file, "w", encoding="utf-8") as f:
            json.dump(webhooks, f, indent=2, default=str)

    def _webhook_from_dict(self, data: dict) -> Webhook:
        """Convert dict to Webhook model"""
        return Webhook(
            id=UUID(data["id"]),
            document_id=UUID(data["document_id"]),
            callback_url=data["callback_url"],
            event_type=data.get("event_type"),
            status=WebhookStatus(data["status"]),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            last_error=data.get("last_error"),
            next_retry_at=datetime.fromisoformat(data["next_retry_at"]) if data.get("next_retry_at") else None,
            delivered_at=datetime.fromisoformat(data["delivered_at"]) if data.get("delivered_at") else None
        )

    async def create(
        self,
        document_id: UUID,
        callback_url: str,
        event_type: str
    ) -> Webhook:
        """Create a new webhook"""
        webhooks = self._load_webhooks()

        webhook_id = uuid.uuid4()

        webhook_data = {
            "id": str(webhook_id),
            "document_id": str(document_id),
            "callback_url": callback_url,
            "event_type": event_type,
            "status": WebhookStatus.PENDING.value,
            "retry_count": 0,
            "max_retries": 3,
            "last_error": None,
            "next_retry_at": None,
            "delivered_at": None
        }

        webhooks[str(webhook_id)] = webhook_data
        self._save_webhooks(webhooks)

        return self._webhook_from_dict(webhook_data)

    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        """Get webhook by ID"""
        webhooks = self._load_webhooks()
        webhook_data = webhooks.get(str(webhook_id))

        if not webhook_data:
            return None

        return self._webhook_from_dict(webhook_data)

    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        """Get all webhooks for a document"""
        webhooks = self._load_webhooks()
        doc_id_str = str(document_id)

        return [
            self._webhook_from_dict(data)
            for data in webhooks.values()
            if data["document_id"] == doc_id_str
        ]

    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        """Get pending webhooks (including due retries)"""
        webhooks = self._load_webhooks()
        now = datetime.now()

        result = []
        for data in webhooks.values():
            if data["status"] != WebhookStatus.PENDING.value:
                continue

            # Check if retry is due
            if data.get("next_retry_at"):
                retry_at = datetime.fromisoformat(data["next_retry_at"])
                if retry_at > now:
                    continue

            result.append(self._webhook_from_dict(data))

        return result[:limit]

    async def mark_delivered(self, webhook_id: UUID) -> bool:
        """Mark webhook as successfully delivered"""
        webhooks = self._load_webhooks()
        webhook_key = str(webhook_id)

        if webhook_key not in webhooks:
            return False

        webhooks[webhook_key]["status"] = WebhookStatus.DELIVERED.value
        webhooks[webhook_key]["delivered_at"] = datetime.now().isoformat()

        self._save_webhooks(webhooks)
        return True

    async def mark_failed(
        self,
        webhook_id: UUID,
        error: str,
        retry_after: Optional[datetime] = None
    ) -> bool:
        """Mark webhook as failed, schedule retry"""
        webhooks = self._load_webhooks()
        webhook_key = str(webhook_id)

        if webhook_key not in webhooks:
            return False

        webhook = webhooks[webhook_key]
        webhook["retry_count"] = webhook.get("retry_count", 0) + 1
        webhook["last_error"] = error

        # Check if we should retry
        if webhook["retry_count"] < webhook.get("max_retries", 3):
            webhook["status"] = WebhookStatus.PENDING.value
            webhook["next_retry_at"] = retry_after.isoformat() if retry_after else None
        else:
            webhook["status"] = WebhookStatus.FAILED.value

        self._save_webhooks(webhooks)
        return True
```

**Step 2: Update __init__.py**

```python
"""Local storage implementations"""
from .document import LocalDocumentStorage
from .task import LocalTaskStorage
from .webhook import LocalWebhookStorage

__all__ = ["LocalDocumentStorage", "LocalTaskStorage", "LocalWebhookStorage"]
```

**Step 3: Commit**

```bash
git add backend/app/storage/local/
git commit -m "feat: implement local webhook storage"
```

---

### Task 2.6: Create Storage Factory

**Files:**
- Create: `backend/app/storage/factory.py`
- Modify: `backend/app/storage/__init__.py`

**Step 1: Create factory.py**

```python
"""Storage factory for creating storage instances based on configuration"""
from typing import Optional

from .base import StorageManager, DocumentStorage, TaskStorage, WebhookStorage
from .local import LocalDocumentStorage, LocalTaskStorage, LocalWebhookStorage


def create_storage_manager(
    backend: str = "local",
    storage_dir: str = "data/storage",
    database_url: Optional[str] = None,
    **kwargs
) -> StorageManager:
    """
    Create a StorageManager based on the specified backend.

    Args:
        backend: "local" or "database"
        storage_dir: Directory for local storage
        database_url: PostgreSQL connection URL (for database backend)
        **kwargs: Additional backend-specific options

    Returns:
        Configured StorageManager instance
    """
    if backend == "local":
        return StorageManager(
            documents=LocalDocumentStorage(storage_dir),
            tasks=LocalTaskStorage(storage_dir),
            webhooks=LocalWebhookStorage(storage_dir)
        )
    elif backend == "database":
        # Database implementation will be added in Phase 3
        raise NotImplementedError("Database backend not yet implemented")
    else:
        raise ValueError(f"Unknown storage backend: {backend}")


# Global storage manager instance
_storage_manager: Optional[StorageManager] = None


def get_storage_manager() -> StorageManager:
    """Get the global storage manager instance"""
    global _storage_manager

    if _storage_manager is None:
        # Import here to avoid circular imports
        from app.config import settings

        _storage_manager = create_storage_manager(
            backend=settings.storage_backend,
            storage_dir=settings.storage_dir,
            database_url=getattr(settings, 'database_url', None)
        )

    return _storage_manager


def reset_storage_manager():
    """Reset the global storage manager (useful for testing)"""
    global _storage_manager
    _storage_manager = None
```

**Step 2: Update main __init__.py**

```python
"""Storage layer package"""
from .models import Document, Task, Webhook, DocumentStatus, TaskStatus, WebhookStatus
from .base import DocumentStorage, TaskStorage, WebhookStorage, StorageManager
from .factory import create_storage_manager, get_storage_manager, reset_storage_manager

__all__ = [
    # Models
    "Document",
    "Task",
    "Webhook",
    "DocumentStatus",
    "TaskStatus",
    "WebhookStatus",
    # Interfaces
    "DocumentStorage",
    "TaskStorage",
    "WebhookStorage",
    "StorageManager",
    # Factory
    "create_storage_manager",
    "get_storage_manager",
    "reset_storage_manager",
]
```

**Step 3: Commit**

```bash
git add backend/app/storage/
git commit -m "feat: add storage factory with configuration-based backend selection"
```

---

## Phase 3: Database Implementation

### Task 3.1: Add Database Dependencies

**Files:**
- Modify: `backend/requirements.txt`

**Step 1: Add asyncpg and related packages**

Append to `backend/requirements.txt`:

```
# Database
asyncpg>=0.29.0
sqlalchemy[asyncio]>=2.0.0
```

**Step 2: Install dependencies**

```bash
pip install asyncpg sqlalchemy[asyncio]
```

**Step 3: Commit**

```bash
git add backend/requirements.txt
git commit -m "feat: add database dependencies (asyncpg, sqlalchemy)"
```

---

### Task 3.2: Implement Database Connection Pool

**Files:**
- Create: `backend/app/storage/database/__init__.py`
- Create: `backend/app/storage/database/connection.py`

**Step 1: Create database directory**

```bash
mkdir -p backend/app/storage/database
```

**Step 2: Create connection.py**

```python
"""Database connection management"""
import asyncpg
from typing import Optional
from contextlib import asynccontextmanager


class DatabasePool:
    """PostgreSQL connection pool manager"""

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def initialize(cls, database_url: str, min_size: int = 5, max_size: int = 20):
        """Initialize the connection pool"""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                database_url,
                min_size=min_size,
                max_size=max_size
            )

    @classmethod
    async def close(cls):
        """Close the connection pool"""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        """Get the connection pool"""
        if cls._pool is None:
            raise RuntimeError("Database pool not initialized. Call initialize() first.")
        return cls._pool

    @classmethod
    @asynccontextmanager
    async def connection(cls):
        """Get a connection from the pool"""
        pool = cls.get_pool()
        async with pool.acquire() as conn:
            yield conn

    @classmethod
    @asynccontextmanager
    async def transaction(cls):
        """Get a connection with transaction"""
        pool = cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                yield conn


async def check_database_health(database_url: str) -> bool:
    """Check if database is accessible"""
    try:
        conn = await asyncpg.connect(database_url)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception:
        return False
```

**Step 3: Create __init__.py**

```python
"""Database storage implementations"""
from .connection import DatabasePool, check_database_health

__all__ = ["DatabasePool", "check_database_health"]
```

**Step 4: Commit**

```bash
git add backend/app/storage/database/
git commit -m "feat: implement database connection pool"
```

---

### Task 3.3: Implement Database Document Storage

**Files:**
- Create: `backend/app/storage/database/document.py`
- Modify: `backend/app/storage/database/__init__.py`

**Step 1: Create document.py**

```python
"""PostgreSQL document storage implementation"""
import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..base import DocumentStorage
from ..models import Document, DocumentStatus
from .connection import DatabasePool


class DatabaseDocumentStorage(DocumentStorage):
    """PostgreSQL-based document storage"""

    async def create(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str
    ) -> Document:
        """Create a new document record"""
        doc_id = uuid.uuid4()
        now = datetime.now()

        async with DatabasePool.connection() as conn:
            await conn.execute(
                """
                INSERT INTO documents (id, filename, file_path, file_size, mime_type, status, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                doc_id, filename, file_path, file_size, mime_type,
                DocumentStatus.PENDING.value, now, now
            )

        return Document(
            id=doc_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            status=DocumentStatus.PENDING,
            created_at=now,
            updated_at=now
        )

    async def get(self, doc_id: UUID) -> Optional[Document]:
        """Get document by ID"""
        async with DatabasePool.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM documents WHERE id = $1",
                doc_id
            )

        if not row:
            return None

        return Document(
            id=row["id"],
            filename=row["filename"],
            file_path=row["file_path"],
            file_size=row["file_size"],
            mime_type=row["mime_type"],
            status=DocumentStatus(row["status"]),
            error_message=row["error_message"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Document]:
        """List documents with optional filtering"""
        async with DatabasePool.connection() as conn:
            if status:
                rows = await conn.fetch(
                    """
                    SELECT * FROM documents
                    WHERE status = $1
                    ORDER BY created_at DESC
                    LIMIT $2 OFFSET $3
                    """,
                    status, limit, offset
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT * FROM documents
                    ORDER BY created_at DESC
                    LIMIT $1 OFFSET $2
                    """,
                    limit, offset
                )

        return [
            Document(
                id=row["id"],
                filename=row["filename"],
                file_path=row["file_path"],
                file_size=row["file_size"],
                mime_type=row["mime_type"],
                status=DocumentStatus(row["status"]),
                error_message=row["error_message"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            for row in rows
        ]

    async def update_status(
        self,
        doc_id: UUID,
        status: str,
        error_message: Optional[str] = None
    ) -> bool:
        """Update document status"""
        async with DatabasePool.connection() as conn:
            if error_message is not None:
                result = await conn.execute(
                    """
                    UPDATE documents
                    SET status = $1, error_message = $2, updated_at = $3
                    WHERE id = $4
                    """,
                    status, error_message, datetime.now(), doc_id
                )
            else:
                result = await conn.execute(
                    """
                    UPDATE documents
                    SET status = $1, updated_at = $2
                    WHERE id = $3
                    """,
                    status, datetime.now(), doc_id
                )

        return result == "UPDATE 1"

    async def delete(self, doc_id: UUID) -> bool:
        """Delete document (cascade deletes tasks and webhooks)"""
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                "DELETE FROM documents WHERE id = $1",
                doc_id
            )

        return result == "DELETE 1"
```

**Step 2: Update __init__.py**

```python
"""Database storage implementations"""
from .connection import DatabasePool, check_database_health
from .document import DatabaseDocumentStorage

__all__ = [
    "DatabasePool",
    "check_database_health",
    "DatabaseDocumentStorage",
]
```

**Step 3: Commit**

```bash
git add backend/app/storage/database/
git commit -m "feat: implement database document storage"
```

---

### Task 3.4: Implement Database Task Storage

**Files:**
- Create: `backend/app/storage/database/task.py`
- Modify: `backend/app/storage/database/__init__.py`

**Step 1: Create task.py**

```python
"""PostgreSQL task storage implementation"""
import uuid
from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID
import json

from ..base import TaskStorage
from ..models import Task, TaskStatus
from .connection import DatabasePool


class DatabaseTaskStorage(TaskStorage):
    """PostgreSQL-based task storage"""

    def _row_to_task(self, row) -> Task:
        """Convert database row to Task model"""
        return Task(
            id=row["id"],
            document_id=row["document_id"],
            task_type=row["task_type"],
            status=TaskStatus(row["status"]),
            progress=row["progress"],
            retry_count=row["retry_count"],
            max_retries=row["max_retries"],
            last_error=row["last_error"],
            result=row["result"],
            created_at=row["created_at"],
            started_at=row["started_at"],
            completed_at=row["completed_at"]
        )

    async def create(self, document_id: UUID, task_type: str) -> Task:
        """Create a new task"""
        task_id = uuid.uuid4()
        now = datetime.now()

        async with DatabasePool.connection() as conn:
            await conn.execute(
                """
                INSERT INTO tasks (id, document_id, task_type, status, progress, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                task_id, document_id, task_type, TaskStatus.PENDING.value, 0, now
            )

        return Task(
            id=task_id,
            document_id=document_id,
            task_type=task_type,
            status=TaskStatus.PENDING,
            progress=0,
            created_at=now
        )

    async def get(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        async with DatabasePool.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM tasks WHERE id = $1",
                task_id
            )

        if not row:
            return None

        return self._row_to_task(row)

    async def get_by_document(self, document_id: UUID) -> List[Task]:
        """Get all tasks for a document"""
        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM tasks
                WHERE document_id = $1
                ORDER BY created_at DESC
                """,
                document_id
            )

        return [self._row_to_task(row) for row in rows]

    async def list_pending(self, limit: int = 10) -> List[Task]:
        """Get pending tasks for processing"""
        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM tasks
                WHERE status = $1
                ORDER BY created_at ASC
                LIMIT $2
                """,
                TaskStatus.PENDING.value, limit
            )

        return [self._row_to_task(row) for row in rows]

    async def start(self, task_id: UUID) -> bool:
        """Mark task as started"""
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                """
                UPDATE tasks
                SET status = $1, started_at = $2
                WHERE id = $3
                """,
                TaskStatus.PROCESSING.value, datetime.now(), task_id
            )

        return result == "UPDATE 1"

    async def update_progress(self, task_id: UUID, progress: int) -> bool:
        """Update task progress (0-100)"""
        progress = max(0, min(100, progress))

        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                "UPDATE tasks SET progress = $1 WHERE id = $2",
                progress, task_id
            )

        return result == "UPDATE 1"

    async def complete(self, task_id: UUID, result: Optional[Any] = None) -> bool:
        """Mark task as completed"""
        now = datetime.now()
        result_json = json.dumps(result) if result else None

        async with DatabasePool.connection() as conn:
            db_result = await conn.execute(
                """
                UPDATE tasks
                SET status = $1, progress = 100, result = $2, completed_at = $3
                WHERE id = $4
                """,
                TaskStatus.COMPLETED.value, result_json, now, task_id
            )

        return db_result == "UPDATE 1"

    async def fail(self, task_id: UUID, error: str) -> bool:
        """Mark task as failed, handle retry logic"""
        async with DatabasePool.transaction() as conn:
            # Get current retry count
            row = await conn.fetchrow(
                "SELECT retry_count, max_retries FROM tasks WHERE id = $1",
                task_id
            )

            if not row:
                return False

            new_retry_count = row["retry_count"] + 1

            if new_retry_count < row["max_retries"]:
                # Retry: set back to pending
                await conn.execute(
                    """
                    UPDATE tasks
                    SET status = $1, retry_count = $2, last_error = $3
                    WHERE id = $4
                    """,
                    TaskStatus.PENDING.value, new_retry_count, error, task_id
                )
            else:
                # Max retries reached: mark as failed
                await conn.execute(
                    """
                    UPDATE tasks
                    SET status = $1, retry_count = $2, last_error = $3, completed_at = $4
                    WHERE id = $5
                    """,
                    TaskStatus.FAILED.value, new_retry_count, error, datetime.now(), task_id
                )

        return True

    async def cancel(self, task_id: UUID) -> bool:
        """Cancel a pending or processing task"""
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                """
                UPDATE tasks
                SET status = $1, completed_at = $2
                WHERE id = $3 AND status IN ($4, $5)
                """,
                TaskStatus.CANCELLED.value, datetime.now(), task_id,
                TaskStatus.PENDING.value, TaskStatus.PROCESSING.value
            )

        return result == "UPDATE 1"
```

**Step 2: Update __init__.py**

```python
"""Database storage implementations"""
from .connection import DatabasePool, check_database_health
from .document import DatabaseDocumentStorage
from .task import DatabaseTaskStorage

__all__ = [
    "DatabasePool",
    "check_database_health",
    "DatabaseDocumentStorage",
    "DatabaseTaskStorage",
]
```

**Step 3: Commit**

```bash
git add backend/app/storage/database/
git commit -m "feat: implement database task storage"
```

---

### Task 3.5: Implement Database Webhook Storage

**Files:**
- Create: `backend/app/storage/database/webhook.py`
- Modify: `backend/app/storage/database/__init__.py`

**Step 1: Create webhook.py**

```python
"""PostgreSQL webhook storage implementation"""
import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..base import WebhookStorage
from ..models import Webhook, WebhookStatus
from .connection import DatabasePool


class DatabaseWebhookStorage(WebhookStorage):
    """PostgreSQL-based webhook storage"""

    def _row_to_webhook(self, row) -> Webhook:
        """Convert database row to Webhook model"""
        return Webhook(
            id=row["id"],
            document_id=row["document_id"],
            callback_url=row["callback_url"],
            event_type=row["event_type"],
            status=WebhookStatus(row["status"]),
            retry_count=row["retry_count"],
            max_retries=row["max_retries"],
            last_error=row["last_error"],
            next_retry_at=row["next_retry_at"],
            delivered_at=row["delivered_at"]
        )

    async def create(
        self,
        document_id: UUID,
        callback_url: str,
        event_type: str
    ) -> Webhook:
        """Create a new webhook"""
        webhook_id = uuid.uuid4()

        async with DatabasePool.connection() as conn:
            await conn.execute(
                """
                INSERT INTO webhooks (id, document_id, callback_url, event_type, status)
                VALUES ($1, $2, $3, $4, $5)
                """,
                webhook_id, document_id, callback_url, event_type, WebhookStatus.PENDING.value
            )

        return Webhook(
            id=webhook_id,
            document_id=document_id,
            callback_url=callback_url,
            event_type=event_type,
            status=WebhookStatus.PENDING
        )

    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        """Get webhook by ID"""
        async with DatabasePool.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM webhooks WHERE id = $1",
                webhook_id
            )

        if not row:
            return None

        return self._row_to_webhook(row)

    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        """Get all webhooks for a document"""
        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM webhooks WHERE document_id = $1",
                document_id
            )

        return [self._row_to_webhook(row) for row in rows]

    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        """Get pending webhooks (including due retries)"""
        now = datetime.now()

        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM webhooks
                WHERE status = $1
                  AND (next_retry_at IS NULL OR next_retry_at <= $2)
                ORDER BY next_retry_at ASC NULLS FIRST
                LIMIT $3
                """,
                WebhookStatus.PENDING.value, now, limit
            )

        return [self._row_to_webhook(row) for row in rows]

    async def mark_delivered(self, webhook_id: UUID) -> bool:
        """Mark webhook as successfully delivered"""
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                """
                UPDATE webhooks
                SET status = $1, delivered_at = $2
                WHERE id = $3
                """,
                WebhookStatus.DELIVERED.value, datetime.now(), webhook_id
            )

        return result == "UPDATE 1"

    async def mark_failed(
        self,
        webhook_id: UUID,
        error: str,
        retry_after: Optional[datetime] = None
    ) -> bool:
        """Mark webhook as failed, schedule retry"""
        async with DatabasePool.transaction() as conn:
            # Get current retry count
            row = await conn.fetchrow(
                "SELECT retry_count, max_retries FROM webhooks WHERE id = $1",
                webhook_id
            )

            if not row:
                return False

            new_retry_count = row["retry_count"] + 1

            if new_retry_count < row["max_retries"]:
                # Retry: keep pending with next retry time
                await conn.execute(
                    """
                    UPDATE webhooks
                    SET retry_count = $1, last_error = $2, next_retry_at = $3
                    WHERE id = $4
                    """,
                    new_retry_count, error, retry_after, webhook_id
                )
            else:
                # Max retries reached: mark as failed
                await conn.execute(
                    """
                    UPDATE webhooks
                    SET status = $1, retry_count = $2, last_error = $3
                    WHERE id = $4
                    """,
                    WebhookStatus.FAILED.value, new_retry_count, error, webhook_id
                )

        return True
```

**Step 2: Update __init__.py**

```python
"""Database storage implementations"""
from .connection import DatabasePool, check_database_health
from .document import DatabaseDocumentStorage
from .task import DatabaseTaskStorage
from .webhook import DatabaseWebhookStorage

__all__ = [
    "DatabasePool",
    "check_database_health",
    "DatabaseDocumentStorage",
    "DatabaseTaskStorage",
    "DatabaseWebhookStorage",
]
```

**Step 3: Commit**

```bash
git add backend/app/storage/database/
git commit -m "feat: implement database webhook storage"
```

---

### Task 3.6: Update Storage Factory for Database Backend

**Files:**
- Modify: `backend/app/storage/factory.py`

**Step 1: Update factory.py to support database backend**

Replace the content with:

```python
"""Storage factory for creating storage instances based on configuration"""
from typing import Optional

from .base import StorageManager, DocumentStorage, TaskStorage, WebhookStorage
from .local import LocalDocumentStorage, LocalTaskStorage, LocalWebhookStorage


_storage_manager: Optional[StorageManager] = None
_database_initialized: bool = False


async def _initialize_database(database_url: str):
    """Initialize database connection pool"""
    global _database_initialized

    if not _database_initialized:
        from .database import DatabasePool
        await DatabasePool.initialize(database_url)
        _database_initialized = True


async def create_storage_manager(
    backend: str = "local",
    storage_dir: str = "data/storage",
    database_url: Optional[str] = None,
    **kwargs
) -> StorageManager:
    """
    Create a StorageManager based on the specified backend.

    Args:
        backend: "local" or "database"
        storage_dir: Directory for local storage
        database_url: PostgreSQL connection URL (for database backend)
        **kwargs: Additional backend-specific options

    Returns:
        Configured StorageManager instance
    """
    if backend == "local":
        return StorageManager(
            documents=LocalDocumentStorage(storage_dir),
            tasks=LocalTaskStorage(storage_dir),
            webhooks=LocalWebhookStorage(storage_dir)
        )
    elif backend == "database":
        if not database_url:
            raise ValueError("database_url is required for database backend")

        # Initialize database connection
        await _initialize_database(database_url)

        from .database import (
            DatabaseDocumentStorage,
            DatabaseTaskStorage,
            DatabaseWebhookStorage
        )

        return StorageManager(
            documents=DatabaseDocumentStorage(),
            tasks=DatabaseTaskStorage(),
            webhooks=DatabaseWebhookStorage()
        )
    else:
        raise ValueError(f"Unknown storage backend: {backend}")


async def get_storage_manager() -> StorageManager:
    """Get the global storage manager instance"""
    global _storage_manager

    if _storage_manager is None:
        from app.config import settings

        _storage_manager = await create_storage_manager(
            backend=settings.storage_backend,
            storage_dir=settings.storage_dir,
            database_url=getattr(settings, 'database_url', None)
        )

    return _storage_manager


async def close_storage():
    """Close storage connections (call on shutdown)"""
    global _storage_manager, _database_initialized

    if _database_initialized:
        from .database import DatabasePool
        await DatabasePool.close()
        _database_initialized = False

    _storage_manager = None


def reset_storage_manager():
    """Reset the global storage manager (useful for testing)"""
    global _storage_manager
    _storage_manager = None
```

**Step 2: Commit**

```bash
git add backend/app/storage/factory.py
git commit -m "feat: update storage factory to support database backend"
```

---

## Phase 4: Integration

### Task 4.1: Add Application Lifecycle Events

**Files:**
- Modify: `backend/app/main.py`

**Step 1: Add startup and shutdown events**

Add the following imports and lifecycle events to `main.py`:

```python
from contextlib import asynccontextmanager
from app.storage import get_storage_manager, close_storage

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await get_storage_manager()  # Initialize storage
    yield
    # Shutdown
    await close_storage()

# Update app creation to use lifespan
app = FastAPI(
    title="Knowledge Graph RAG API",
    lifespan=lifespan,
    # ... other options
)
```

**Step 2: Commit**

```bash
git add backend/app/main.py
git commit -m "feat: add application lifecycle for storage initialization"
```

---

### Task 4.2: Create Storage Dependency

**Files:**
- Modify: `backend/app/dependencies.py`

**Step 1: Add storage dependency function**

Add to `dependencies.py`:

```python
from app.storage import StorageManager, get_storage_manager

async def get_storage() -> StorageManager:
    """FastAPI dependency for storage manager"""
    return await get_storage_manager()
```

**Step 2: Commit**

```bash
git add backend/app/dependencies.py
git commit -m "feat: add FastAPI dependency for storage manager"
```

---

### Task 4.3: Update V1 Documents API to Use Storage Layer

**Files:**
- Modify: `backend/app/api/v1/documents.py`

**Step 1: Update imports and add storage dependency**

This task involves refactoring the documents API to use the new storage abstraction layer instead of direct memory/file access. The changes include:

1. Import the storage dependency
2. Replace direct `_document_store` access with `storage.documents` calls
3. Update all CRUD operations to use the new async interface

**Step 2: Commit**

```bash
git add backend/app/api/v1/documents.py
git commit -m "refactor: update documents API to use storage abstraction layer"
```

---

### Task 4.4: Update V1 Tasks API to Use Storage Layer

**Files:**
- Modify: `backend/app/api/v1/tasks.py`

Similar refactoring as Task 4.3 for the tasks API.

**Step 1: Update to use storage.tasks**

**Step 2: Commit**

```bash
git add backend/app/api/v1/tasks.py
git commit -m "refactor: update tasks API to use storage abstraction layer"
```

---

### Task 4.5: End-to-End Verification

**Step 1: Start services with local backend**

```bash
# Ensure STORAGE_BACKEND=local in .env
python -m uvicorn app.main:app --reload
```

**Step 2: Test document upload**

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "X-API-Key: your-key" \
  -F "file=@test.pdf"
```

**Step 3: Test document list**

```bash
curl http://localhost:8000/api/v1/documents \
  -H "X-API-Key: your-key"
```

**Step 4: Start services with database backend**

```bash
# Set STORAGE_BACKEND=database in .env
# Ensure docker-compose services are running
docker-compose up -d
python -m uvicorn app.main:app --reload
```

**Step 5: Repeat tests 2-3 with database backend**

**Step 6: Verify data in PostgreSQL**

```bash
docker-compose exec postgres psql -U rag -d ragdb -c "SELECT * FROM documents"
```

---

## Summary

**Total Tasks:** 19 tasks across 4 phases

**Phase 1 (Infrastructure):** 4 tasks
- Docker Compose setup
- Database init script
- Environment configuration
- Infrastructure verification

**Phase 2 (Storage Abstraction):** 6 tasks
- Storage models
- Abstract interfaces
- Local document/task/webhook storage
- Storage factory

**Phase 3 (Database Implementation):** 6 tasks
- Database dependencies
- Connection pool
- Database document/task/webhook storage
- Factory update

**Phase 4 (Integration):** 3 tasks
- Application lifecycle
- Storage dependency
- API updates and verification

**Files Created:** 15+ new files
**Files Modified:** 5+ existing files
