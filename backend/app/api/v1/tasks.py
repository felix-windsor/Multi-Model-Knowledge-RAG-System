"""V1 任务管理 API"""
from fastapi import APIRouter, Depends, HTTPException
from app.services.task_service import TaskService, TaskStatus
from app.middleware.auth import verify_api_key
from app.middleware.response import wrap_response, ErrorCode
from app.models.response import V1TaskData

router = APIRouter()


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    查询任务状态

    - **task_id**: 任务 ID
    """
    task = TaskService.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.TASK_NOT_FOUND,
                message=f"任务不存在: {task_id}"
            )
        )

    return wrap_response(
        data=V1TaskData(
            task_id=task["task_id"],
            doc_id=task["doc_id"],
            status=task["status"],
            progress=task["progress"],
            step=task["step"],
            created_at=task.get("created_at"),
            updated_at=task.get("updated_at"),
            error_message=task.get("error_message")
        ).model_dump()
    )


@router.delete("/{task_id}")
async def cancel_task(
    task_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    取消任务

    - **task_id**: 任务 ID

    注意: 只能取消 pending 或 processing 状态的任务
    """
    task = TaskService.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.TASK_NOT_FOUND,
                message=f"任务不存在: {task_id}"
            )
        )

    # 检查任务状态
    if task["status"] not in [TaskStatus.PENDING.value, TaskStatus.PROCESSING.value]:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_PARAMETER,
                message=f"无法取消 {task['status']} 状态的任务"
            )
        )

    success = TaskService.cancel_task(task_id)

    if not success:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.INTERNAL_ERROR,
                message="取消任务失败"
            )
        )

    return wrap_response(
        data={"task_id": task_id, "status": TaskStatus.CANCELLED.value},
        message="Task cancelled successfully"
    )
