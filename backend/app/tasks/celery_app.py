"""Celery application for background document processing"""
import os
import asyncio
from celery import Celery
from kombu import Queue

# Get configuration from environment
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

# Create Celery app
celery_app = Celery(
    'rag_tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['app.tasks.document_tasks']
)

# Configure Celery
celery_app.conf.update(
    # Task settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,

    # Task execution
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    task_soft_time_limit=3300,  # 55 minutes soft limit

    # Worker settings
    worker_prefetch_multiplier=1,  # Take one task at a time
    worker_max_tasks_per_child=50,  # Restart worker after 50 tasks

    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    result_backend_transport_options={
        'master_name': 'mymaster'
    },

    # Task routing with priority queues
    task_routes={
        'app.tasks.document_tasks.process_document_task': {
            'queue': 'document_processing',
            'routing_key': 'document.process'
        },
        'app.tasks.document_tasks.process_batch_task': {
            'queue': 'batch_processing',
            'routing_key': 'batch.process'
        }
    },

    # Define queues with priorities
    task_queues=(
        Queue('document_processing', routing_key='document.#', priority=10),
        Queue('batch_processing', routing_key='batch.#', priority=5),
    ),

    # Retry settings
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup"""
    print(f'Request: {self.request!r}')
    return 'Celery is working!'
