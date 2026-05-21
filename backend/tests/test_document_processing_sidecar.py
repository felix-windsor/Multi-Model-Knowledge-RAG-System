import uuid
import asyncio

import pytest

from app.api.v1.documents import process_document_with_callback


class FakeRAG:
    def __init__(self):
        self.processed_files = []
        self.llm_model_func = self.fake_llm

    async def process_document_complete(self, file_path, **kwargs):
        self.processed_files.append({"file_path": file_path, "kwargs": kwargs})

    async def parse_document(self, file_path, display_stats=False, **kwargs):
        return [
            {
                "type": "text",
                "text": "综合管理系统通过统一身份认证平台完成用户登录，并将操作日志写入审计服务。",
            }
        ], "parsed-doc-1"

    async def fake_llm(self, prompt, **kwargs):
        return {
            "entities": [
                {"name": "综合管理系统", "type": "业务系统"},
                {"name": "统一身份认证平台", "type": "平台"},
            ],
            "relations": [
                {"source": "综合管理系统", "target": "统一身份认证平台", "type": "使用"}
            ],
        }


class FakeTaskService:
    def __init__(self):
        self.progress_events = []
        self.completed_result = None
        self.failed_error = None

    async def start_task(self, task_id):
        return True

    async def update_progress(self, task_id, progress, step=None):
        self.progress_events.append({"progress": progress, "step": step})
        return True

    async def complete_task(self, task_id, result=None):
        self.completed_result = result
        return True

    async def fail_task(self, task_id, error):
        self.failed_error = error
        return True


class FakeWebhookService:
    async def deliver_document_event(self, *args, **kwargs):
        return True


class BlockingFakeRAG(FakeRAG):
    def __init__(self):
        super().__init__()
        self.active_count = 0
        self.max_active_count = 0
        self.started_count = 0
        self.first_started = asyncio.Event()
        self.release_first = asyncio.Event()

    async def process_document_complete(self, file_path, **kwargs):
        self.active_count += 1
        self.started_count += 1
        self.max_active_count = max(self.max_active_count, self.active_count)
        self.processed_files.append({"file_path": file_path, "kwargs": kwargs})
        if self.started_count == 1:
            self.first_started.set()
            await self.release_first.wait()
        await asyncio.sleep(0)
        self.active_count -= 1


@pytest.mark.asyncio
async def test_process_document_with_callback_adds_sidecar_report_when_enabled():
    task_svc = FakeTaskService()

    await process_document_with_callback(
        rag=FakeRAG(),
        doc_id=uuid.uuid4(),
        task_id=uuid.uuid4(),
        file_path="/tmp/example.md",
        callback_url=None,
        task_svc=task_svc,
        webhook_svc=FakeWebhookService(),
        extraction_sidecar_enabled=True,
        extraction_sidecar_max_chars=1200,
    )

    assert task_svc.failed_error is None
    assert task_svc.completed_result["extraction_sidecar"]["enabled"] is True
    assert task_svc.completed_result["extraction_sidecar"]["chunk_count"] == 1
    assert task_svc.completed_result["extraction_sidecar"]["aggregate"]["entity_type_drift_count"] == 1
    assert task_svc.completed_result["extraction_sidecar"]["aggregate"]["relation_type_drift_count"] == 1
    assert {"progress": 92, "step": "正在生成抽取质量报告"} in task_svc.progress_events


@pytest.mark.asyncio
async def test_process_document_with_callback_limits_concurrent_processing():
    rag = BlockingFakeRAG()
    first_task_svc = FakeTaskService()
    second_task_svc = FakeTaskService()

    first = asyncio.create_task(
        process_document_with_callback(
            rag=rag,
            doc_id=uuid.uuid4(),
            task_id=uuid.uuid4(),
            file_path="/tmp/first.md",
            callback_url=None,
            task_svc=first_task_svc,
            webhook_svc=FakeWebhookService(),
            max_concurrent_tasks=1,
        )
    )
    await rag.first_started.wait()

    second = asyncio.create_task(
        process_document_with_callback(
            rag=rag,
            doc_id=uuid.uuid4(),
            task_id=uuid.uuid4(),
            file_path="/tmp/second.md",
            callback_url=None,
            task_svc=second_task_svc,
            webhook_svc=FakeWebhookService(),
            max_concurrent_tasks=1,
        )
    )
    await asyncio.sleep(0.05)

    assert rag.started_count == 1
    assert {"progress": 1, "step": "等待文档处理并发槽位"} in second_task_svc.progress_events

    rag.release_first.set()
    await asyncio.gather(first, second)

    assert rag.started_count == 2
    assert rag.max_active_count == 1
