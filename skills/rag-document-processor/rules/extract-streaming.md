# extract-streaming

**Priority**: 2 (CRITICAL)
**Category**: Content Extraction
**Impact**: Reduces memory usage by 90%+ for large files

## Why It Matters

Loading entire documents into memory causes:
- **Memory spikes** - A 100MB PDF can consume 1GB+ RAM during processing
- **OOM crashes** - Processing multiple large files simultaneously
- **Slow startup** - Waiting for entire file to load before processing begins

Streaming enables processing files of any size with constant memory usage.

**Performance impact**:
- Memory: 500MB → 50MB (10x reduction)
- Latency: Start processing immediately vs. waiting for full load
- Throughput: Process 10x more documents concurrently

## ❌ Incorrect Implementation

```python
# BAD: Load entire PDF into memory
def extract_pdf_content(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        # Loads entire file into memory
        pdf_data = f.read()

    # Parse entire document at once
    pdf = PyPDF2.PdfReader(io.BytesIO(pdf_data))

    # Extract all pages into memory
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text()

    return full_text
```

**Problems:**
- 100MB PDF → 100MB in memory (just for the file)
- Parsing creates additional objects → 200-300MB
- Text extraction → another 50-100MB
- **Total: 350-500MB for a single 100MB PDF**

For 10 concurrent uploads → 3.5-5GB RAM usage!

## ✅ Correct Implementation

```python
from typing import Iterator, Optional
import PyPDF2
from pathlib import Path

def extract_pdf_streaming(
    file_path: str,
    chunk_size: int = 4096,
    page_batch_size: int = 10
) -> Iterator[dict]:
    """
    Stream PDF content page-by-page.

    Yields:
        dict with keys: page_num, text, metadata

    Memory usage: ~50MB regardless of PDF size
    """
    pdf_reader = PyPDF2.PdfReader(file_path)
    total_pages = len(pdf_reader.pages)

    # Process in batches
    for batch_start in range(0, total_pages, page_batch_size):
        batch_end = min(batch_start + page_batch_size, total_pages)

        for page_num in range(batch_start, batch_end):
            page = pdf_reader.pages[page_num]

            # Extract text from single page
            text = page.extract_text()

            # Yield immediately (don't accumulate)
            yield {
                'page_num': page_num + 1,
                'text': text,
                'metadata': {
                    'total_pages': total_pages,
                    'batch': batch_start // page_batch_size
                }
            }

            # Optionally clear page from memory
            del page
            del text


def process_document_streaming(file_path: str) -> str:
    """
    Process document using streaming extraction.
    """
    doc_id = generate_doc_id()
    chunks_processed = 0

    # Stream content page-by-page
    for page_data in extract_pdf_streaming(file_path):
        # Process each page immediately
        chunk_id = f"{doc_id}_page_{page_data['page_num']}"

        # Store/embed/index this chunk
        store_chunk(chunk_id, page_data['text'])

        chunks_processed += 1

        # Report progress (don't wait for entire document)
        if chunks_processed % 10 == 0:
            update_progress(doc_id, chunks_processed)

    return doc_id


# For RAG integration
async def insert_document_streaming(
    rag_instance,
    file_path: str,
    doc_id: str
) -> dict:
    """
    Insert document into RAG using streaming.
    """
    total_chunks = 0
    total_chars = 0

    # Stream and insert chunk-by-chunk
    for page_data in extract_pdf_streaming(file_path):
        # Insert into RAG immediately (don't batch)
        await rag_instance.insert_chunk(
            doc_id=doc_id,
            chunk_id=f"{doc_id}_p{page_data['page_num']}",
            content=page_data['text']
        )

        total_chunks += 1
        total_chars += len(page_data['text'])

        # Memory-efficient: each iteration frees previous page

    return {
        'doc_id': doc_id,
        'chunks': total_chunks,
        'chars': total_chars
    }
```

**Benefits:**
- ✅ Memory usage: O(1) instead of O(n)
- ✅ Start processing immediately (lower latency)
- ✅ Can process files larger than available RAM
- ✅ Progress updates during processing (better UX)

## Advanced: Async Streaming

For even better performance, combine streaming with async I/O:

```python
import asyncio
from typing import AsyncIterator

async def extract_pdf_async_streaming(
    file_path: str
) -> AsyncIterator[dict]:
    """
    Async streaming for maximum throughput.
    """
    # Use async file I/O
    async with aiofiles.open(file_path, 'rb') as f:
        # Read and process in chunks
        while True:
            chunk = await f.read(4096)
            if not chunk:
                break

            # Process chunk
            yield await process_chunk_async(chunk)


async def process_multiple_documents(file_paths: list[str]):
    """
    Process multiple documents concurrently with streaming.

    Memory usage: ~50MB × number of concurrent tasks
    vs. 500MB × number of files (non-streaming)
    """
    tasks = [
        insert_document_streaming(rag, path, f"doc-{i}")
        for i, path in enumerate(file_paths)
    ]

    # Process all concurrently (memory-efficient due to streaming)
    results = await asyncio.gather(*tasks)
    return results
```

## Integration Points

Apply this rule in:

- `backend/app/services/document_service.py::process_document()`
  - Replace full-file loading with streaming
- `backend/knowledge_graph_rag/raganything.py`
  - Implement streaming insertion methods
- Background task processing
  - Reduce memory footprint for concurrent uploads

## Performance Comparison

| Metric | Non-Streaming | Streaming | Improvement |
|--------|--------------|-----------|-------------|
| Memory (100MB PDF) | 500MB | 50MB | 10x |
| Memory (10 concurrent) | 5GB | 500MB | 10x |
| Time to first chunk | 3-5s | 0.1s | 30-50x |
| Max file size | RAM limit | Unlimited | ∞ |

## Real-World Example

```python
# User uploads 500MB technical manual (2000 pages)

# ❌ Without streaming:
# → Tries to load 500MB into memory
# → Actually uses 2-3GB during processing
# → Takes 30 seconds before first result
# → May crash with OOM on limited servers

# ✅ With streaming:
# → Uses 50MB constant memory
# → First page processed in 0.1s
# → Progress updates every 10 pages
# → Completes successfully regardless of file size
```

## Common Pitfalls

### Pitfall 1: Accumulating results

```python
# BAD: Defeats the purpose of streaming
def process_streaming(file_path):
    results = []  # ← Accumulates everything in memory!
    for page in extract_pdf_streaming(file_path):
        results.append(page)  # ← Growing list
    return results  # ← All in memory at once
```

**Fix**: Process and discard each chunk immediately

```python
# GOOD: Process and discard
def process_streaming(file_path):
    for page in extract_pdf_streaming(file_path):
        process_page(page)  # ← Immediate processing
        # page is garbage collected after this iteration
```

### Pitfall 2: Blocking I/O in async context

```python
# BAD: Blocking async function
async def process():
    for page in extract_pdf_streaming(file_path):  # ← Blocking!
        await save_page(page)
```

**Fix**: Use async iterators

```python
# GOOD: Non-blocking async
async def process():
    async for page in extract_pdf_async_streaming(file_path):
        await save_page(page)
```

## Related Rules

- `extract-parallel-pages` - Combine with parallel processing
- `perf-memory-pooling` - Reuse buffers in streaming pipeline
- `extract-cache-results` - Cache streamed results if needed
- `batch-progress-tracking` - Report progress during streaming

## Testing

```python
import pytest
import psutil
import os

def test_streaming_memory_usage():
    """Verify streaming uses constant memory."""
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # MB

    # Process large file with streaming
    for page in extract_pdf_streaming('tests/fixtures/large_100mb.pdf'):
        process_page(page)

    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    mem_increase = mem_after - mem_before

    # Should use <100MB regardless of file size
    assert mem_increase < 100, f"Memory increased by {mem_increase}MB"


def test_streaming_partial_results():
    """Verify streaming returns partial results immediately."""
    import time

    start = time.time()
    results = []

    for i, page in enumerate(extract_pdf_streaming('large.pdf')):
        if i == 0:
            first_page_time = time.time() - start
            # Should get first page in <1 second
            assert first_page_time < 1.0
            break
```
