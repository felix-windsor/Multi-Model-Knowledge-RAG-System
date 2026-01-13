"""Celery tasks for document processing"""
import asyncio
import os
from typing import Dict, Any
from celery import Task
from app.tasks.celery_app import celery_app
from app.dependencies import get_rag_instance
from app.services.document_service import DocumentService


class AsyncTask(Task):
    """Base task class that properly handles async functions"""

    def __call__(self, *args, **kwargs):
        """Override call to run async functions in event loop"""
        return asyncio.run(self.run_async(*args, **kwargs))

    async def run_async(self, *args, **kwargs):
        """Override this method in subclasses"""
        raise NotImplementedError


@celery_app.task(
    bind=True,
    base=AsyncTask,
    name='app.tasks.document_tasks.process_document_task',
    max_retries=3,
    default_retry_delay=60
)
async def process_document_task(
    self,
    doc_id: str,
    file_path: str,
    filename: str
) -> Dict[str, Any]:
    """
    Background task: Process a single document

    Args:
        doc_id: Document ID
        file_path: Path to uploaded file
        filename: Original filename

    Returns:
        Processing result dictionary
    """
    try:
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'doc_id': doc_id,
                'status': 'processing',
                'progress': 10,
                'step': '开始处理文档'
            }
        )

        # Get RAG instance
        rag = await get_rag_instance()
        DocumentService.set_rag_instance(rag)

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'doc_id': doc_id,
                'status': 'processing',
                'progress': 20,
                'step': '正在解析文档'
            }
        )

        # Process document
        result = await rag.process_document_complete(file_path)

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'doc_id': doc_id,
                'status': 'processing',
                'progress': 90,
                'step': '正在更新文档状态'
            }
        )

        # Update document status
        await DocumentService.update_document_status(
            doc_id=doc_id,
            status='completed',
            chunks_count=result.get('chunks_count', 0)
        )

        return {
            'doc_id': doc_id,
            'status': 'completed',
            'filename': filename,
            'chunks_count': result.get('chunks_count', 0),
            'message': '文档处理成功'
        }

    except Exception as e:
        # Update failed status
        await DocumentService.update_document_status(
            doc_id=doc_id,
            status='failed',
            error=str(e)
        )

        # Retry if not max retries
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        return {
            'doc_id': doc_id,
            'status': 'failed',
            'filename': filename,
            'error': str(e)
        }


@celery_app.task(
    bind=True,
    base=AsyncTask,
    name='app.tasks.document_tasks.process_batch_task',
    max_retries=1
)
async def process_batch_task(
    self,
    folder_path: str,
    recursive: bool = True,
    max_workers: int = 2
) -> Dict[str, Any]:
    """
    Background task: Process multiple documents in a folder

    Args:
        folder_path: Path to folder containing documents
        recursive: Whether to process subfolders
        max_workers: Number of parallel workers

    Returns:
        Batch processing result
    """
    try:
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'processing',
                'progress': 10,
                'step': '开始批量处理'
            }
        )

        # Get RAG instance
        rag = await get_rag_instance()

        # Process folder
        result = await rag.process_folder_complete(
            folder_path=folder_path,
            recursive=recursive,
            max_workers=max_workers
        )

        return {
            'status': 'completed',
            'processed_count': result.get('processed_count', 0),
            'failed_count': result.get('failed_count', 0),
            'message': '批量处理完成'
        }

    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }


@celery_app.task(name='app.tasks.document_tasks.cleanup_temp_files')
def cleanup_temp_files(older_than_hours: int = 24):
    """
    Periodic task: Clean up temporary files

    Args:
        older_than_hours: Delete files older than this many hours
    """
    import time
    from pathlib import Path

    upload_dir = Path("../data/uploads")
    current_time = time.time()
    cutoff_time = current_time - (older_than_hours * 3600)

    deleted_count = 0
    for file_path in upload_dir.glob("*"):
        if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    return {
        'status': 'completed',
        'deleted_count': deleted_count,
        'message': f'Cleaned up {deleted_count} temporary files'
    }
