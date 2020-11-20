import os
import logging

from celery import shared_task, current_task
from .services.task_service import execute_diffing_task
from .constants.metrics import METRIC_CSV

log = logging.getLogger(__name__)


@shared_task()
def diffing_task(metric_id):
    if metric_id not in METRIC_CSV:
        log.error(f'Metric {metric_id} not valid')
        return False

    current_task_id = current_task.request.id
    execute_diffing_task(metric_id, METRIC_CSV[metric_id], current_task_id)
