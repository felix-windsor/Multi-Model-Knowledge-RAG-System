"""V1 任务管理 API（重构版 - 使用 Service DI）"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_task_service
from app.middleware.auth import verify_api_key
from app.middleware.response import ErrorCode, wrap_response
from app.models.response import V1TaskData
from app.services.task_service import TaskService
from app.storage.models import TaskStatus

router = APIRouter()


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    task_svc: TaskService = Depends(get_task_service),
    api_key: str = Depends(verify_api_key),
):
    """
    查询任务状态

    - **task_id**: 任务 ID
    """
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_PARAMETER,
                message=f"无效的任务 ID 格式: {task_id}",
            ),
        )

    task = await task_svc.get_task(uuid_task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.TASK_NOT_FOUND,
                message=f"任务不存在: {task_id}",
            ),
        )

    return wrap_response(
        data=V1TaskData(
            task_id=str(task.id),
            doc_id=str(task.document_id),
            status=task.status.value,
            progress=task.progress,
            step=task.step or "等待处理",
            created_at=task.created_at.isoformat() if task.created_at else None,
            updated_at=None,
            error_message=task.last_error,
        ).model_dump()
    )


@router.delete("/{task_id}")
async def cancel_task(
    task_id: str,
    task_svc: TaskService = Depends(get_task_service),
    api_key: str = Depends(verify_api_key),
):
    """
    取消任务

    - **task_id**: 任务 ID

    注意: 只能取消 pending 或 processing 状态的任务
    """
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_PARAMETER,
                message=f"无效的任务 ID 格式: {task_id}",
            ),
        )

    task = await task_svc.get_task(uuid_task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.TASK_NOT_FOUND,
                message=f"任务不存在: {task_id}",
            ),
        )

    # 检查任务状态
    if task.status not in [TaskStatus.PENDING, TaskStatus.PROCESSING]:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_PARAMETER,
                message=f"无法取消 {task.status.value} 状态的任务",
            ),
        )

    success = await task_svc.cancel_task(uuid_task_id)

    if not success:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.INTERNAL_ERROR,
                message="取消任务失败",
            ),
        )

    return wrap_response(
        data={"task_id": task_id, "status": TaskStatus.CANCELLED.value},
        message="Task cancelled successfully",
    )
