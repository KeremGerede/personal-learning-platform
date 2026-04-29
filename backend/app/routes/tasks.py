from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.patch("/{task_id}/complete", response_model=schemas.TaskResponse)
def update_task_completion(
    task_id: int,
    is_completed: bool,
    db: Session = Depends(get_db)
):
    task = db.query(models.PlanTask).filter(
        models.PlanTask.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı.")

    task.is_completed = is_completed
    db.commit()
    db.refresh(task)

    return task