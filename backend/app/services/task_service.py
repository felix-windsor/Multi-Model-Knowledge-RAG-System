"""任务管理服务"""
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# 任务存储（内存存储，生产环境应使用数据库）
_task_store: Dict[str, Dict[str, Any]] = {}


class TaskService:
    """任务管理服务"""

    @staticmethod
    def generate_task_id() -> str:
        """生成任务 ID"""
        return f"task_{uuid.uuid4().hex[:12]}"

    @staticmethod
    def create_task(
        doc_id: str,
        task_type: str = "document_processing",
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建新任务

        Args:
            doc_id: 关联的文档 ID
            task_type: 任务类型
            callback_url: Webhook 回调 URL

        Returns:
            任务信息字典
        """
        task_id = TaskService.generate_task_id()
        now = datetime.now()

        task = {
            "task_id": task_id,
            "doc_id": doc_id,
            "task_type": task_type,
            "status": TaskStatus.PENDING.value,
            "progress": 0,
            "step": "任务已创建",
            "callback_url": callback_url,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "completed_at": None,
            "error_message": None,
            "result": None
        }

        _task_store[task_id] = task
        return task

    @staticmethod
    def get_task(task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务信息"""
        return _task_store.get(task_id)

    @staticmethod
    def get_task_by_doc_id(doc_id: str) -> Optional[Dict[str, Any]]:
        """根据文档 ID 获取最新任务"""
        tasks = [t for t in _task_store.values() if t["doc_id"] == doc_id]
        if not tasks:
            return None
        # 返回最新的任务
        return max(tasks, key=lambda t: t["created_at"])

    @staticmethod
    def update_task(
        task_id: str,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        step: Optional[str] = None,
        error_message: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        更新任务状态

        Args:
            task_id: 任务 ID
            status: 新状态
            progress: 进度 (0-100)
            step: 当前步骤描述
            error_message: 错误信息
            result: 任务结果

        Returns:
            更新后的任务信息
        """
        if task_id not in _task_store:
            return None

        task = _task_store[task_id]
        now = datetime.now()

        if status is not None:
            task["status"] = status

        if progress is not None:
            task["progress"] = progress

        if step is not None:
            task["step"] = step

        if error_message is not None:
            task["error_message"] = error_message

        if result is not None:
            task["result"] = result

        task["updated_at"] = now.isoformat()

        # 如果任务完成或失败，记录完成时间
        if status in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value, TaskStatus.CANCELLED.value]:
            task["completed_at"] = now.isoformat()

        return task

    @staticmethod
    def cancel_task(task_id: str) -> bool:
        """
        取消任务

        Args:
            task_id: 任务 ID

        Returns:
            是否成功取消
        """
        if task_id not in _task_store:
            return False

        task = _task_store[task_id]

        # 只能取消 pending 或 processing 状态的任务
        if task["status"] not in [TaskStatus.PENDING.value, TaskStatus.PROCESSING.value]:
            return False

        TaskService.update_task(
            task_id,
            status=TaskStatus.CANCELLED.value,
            step="任务已取消"
        )

        return True

    @staticmethod
    def get_all_tasks(
        status_filter: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        获取所有任务

        Args:
            status_filter: 状态过滤
            limit: 最大返回数量

        Returns:
            任务列表
        """
        tasks = list(_task_store.values())

        if status_filter:
            tasks = [t for t in tasks if t["status"] == status_filter]

        # 按创建时间倒序排序
        tasks.sort(key=lambda t: t["created_at"], reverse=True)

        return tasks[:limit]

    @staticmethod
    def cleanup_old_tasks(max_age_hours: int = 24):
        """
        清理旧任务

        Args:
            max_age_hours: 最大保留时间（小时）
        """
        now = datetime.now()
        to_delete = []

        for task_id, task in _task_store.items():
            created_at = datetime.fromisoformat(task["created_at"])
            age_hours = (now - created_at).total_seconds() / 3600

            # 只清理已完成/失败/取消的任务
            if task["status"] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value, TaskStatus.CANCELLED.value]:
                if age_hours > max_age_hours:
                    to_delete.append(task_id)

        for task_id in to_delete:
            del _task_store[task_id]
