import logging
import os

from celery.result import AsyncResult
from ..services import diffing_service as dp
from ..utils import csv, file

log = logging.getLogger(__name__)


def get_task_by_id(task_id):
    log.info(f'Getting task by id {task_id}')
    return AsyncResult(task_id)


def execute_diffing_task(metric_id, metric_csv, task_id):
    log.info(f'Running diffing_task for the metric {metric_id}')

    path = file.get_assets_folder()
    csv_folder = os.path.join(path, 'input')
    group_columns = metric_csv['group_columns']
    columns = metric_csv['columns']
    date_column = metric_csv['date_column']
    old_df = csv.load_df(os.path.join(csv_folder, metric_csv['old']))
    new_df = csv.load_df(os.path.join(csv_folder, metric_csv['new']))

    df_result = dp.diffing_process(old_df=old_df, new_df=new_df, columns=columns,
                                   group_columns=group_columns, date_column=date_column)
    csv_created = None
    if not df_result.empty:
        csv_created = csv.create_csv(os.path.join(path, 'output', f'{task_id}.csv'), df_result)

    return csv_created
