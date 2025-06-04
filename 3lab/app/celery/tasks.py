from celery import shared_task
from app.services.task_service import solve_tsp
import time

@shared_task(bind=True)
def tsp_task(self, nodes, edges):
    self.update_state(state="PROGRESS", meta={"progress": 0})
    result = solve_tsp(nodes, edges)
    return result