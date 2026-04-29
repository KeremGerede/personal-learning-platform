from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)


@router.get("/overview", response_model=schemas.StatsOverviewResponse)
def get_stats_overview(db: Session = Depends(get_db)):
    """
    Sistemdeki genel istatistikleri döndürür.

    Şu an authentication olmadığı için tüm kayıtlı planlar ve görevler
    üzerinden genel bir özet hesaplanır.
    """

    total_plans = db.query(models.LearningPlan).count()
    total_tasks = db.query(models.PlanTask).count()

    completed_tasks = (
        db.query(models.PlanTask)
        .filter(models.PlanTask.is_completed == True)
        .count()
    )

    if total_tasks == 0:
        overall_progress_percentage = 0
    else:
        overall_progress_percentage = round(
            (completed_tasks / total_tasks) * 100,
            2
        )

    return {
        "total_plans": total_plans,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overall_progress_percentage": overall_progress_percentage
    }