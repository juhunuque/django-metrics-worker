import os
import logging

from django.http import JsonResponse, HttpResponse
from pandas.errors import EmptyDataError
from diffing.models import Job
from ..tasks import diffing_task
from ..services.task_service import get_task_by_id
from ..utils.csv import load_df
from ..utils.file import get_assets_folder, is_file_exists
from ..constants.metrics import METRIC_CSV


log = logging.getLogger(__name__)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def new_job(request, metric_id):
    log.info(f'Running new_job for the metric {metric_id}')
    if metric_id not in METRIC_CSV:
        return JsonResponse({"error": 'The metric id is not valid.'}, status=400)
    task = diffing_task.delay(metric_id)
    job = Job.objects.create(metric=metric_id, job_id=task.id)
    return JsonResponse({"job_id": job.pk, "metric_id": metric_id})


def get_job(request, job_id):
    log.info(f'Running get_job for the job {job_id}')
    try:
        job = Job.objects.get(pk=int(job_id))
        job_status = get_task_by_id(job.job_id).status
        log.info(f'Job status: {job_status}')

        # If the job is finished successfully
        if str(job_status).lower() == 'success':
            filename = f'{job.job_id}.csv'
            csv_path = os.path.join(get_assets_folder(), 'output', filename)
            if not is_file_exists(csv_path):
                raise FileNotFoundError(f'File does not exist: {csv_path}')

            df = load_df(csv_path)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            df.to_csv(path_or_buf=response)
            return response

        # Otherwise return the current status
        return JsonResponse({"job_id": job_id, "metric_id": job.metric, "status": job_status}, status=404)
    except Job.DoesNotExist:
        return JsonResponse({"job_id": None, "status": 'Job does not exist'}, status=400)
    except FileNotFoundError:
        return JsonResponse({"job_id": None, "status": 'File does not exist'}, status=400)
    except EmptyDataError:
        return JsonResponse({"job_id": None, "status": 'File does not exist'}, status=400)
