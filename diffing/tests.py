import os
import pandas as pd

from django.test import TestCase
from .services.task_service import execute_diffing_task
from .tasks import diffing_task
from .constants.metrics import METRIC_CSV_TEST
from .utils import file, csv


def remove_file(path):
    if file.is_file_exists(path):
        file.remove_file(path)


class TaskServiceTest(TestCase):

    def setUp(self):
        self.revenue_id = 'revenue'
        self.c_revenue_id = 'c_revenue'
        self.task_id = 'b4832752-b772-4c1c-97a5-1cc00abf347d'

        assets_folder = file.get_assets_folder()
        self.input_folder = os.path.join(assets_folder, 'input')
        self.output_folder = os.path.join(assets_folder, 'output')
        self.output_file = os.path.join(self.output_folder, f'{self.task_id}.csv')

        self.metrics_revenue = METRIC_CSV_TEST[self.revenue_id]
        self.metrics_c_revenue = METRIC_CSV_TEST[self.c_revenue_id]
        self.revenue_new_path = os.path.join(self.input_folder, self.metrics_revenue['new'])
        self.revenue_old_path = os.path.join(self.input_folder, self.metrics_revenue['old'])
        self.c_revenue_new_path = os.path.join(self.input_folder, self.metrics_c_revenue['new'])
        self.c_revenue_old_path = os.path.join(self.input_folder, self.metrics_c_revenue['old'])

        # Cleaning previous test data
        remove_file(self.revenue_new_path)
        remove_file(self.revenue_old_path)
        remove_file(self.c_revenue_new_path)
        remove_file(self.c_revenue_old_path)

        # Create fake data sets
        revenue_new_data = [
            ['2020-08-03', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-new-30', 41409.55],
            ['2020-08-04', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-30', 65398.69],
            ['2020-08-04', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-new-30', 41554.95],
            ['2020-08-04', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-ret-30', 23843.739999999998],
            ['2020-08-05', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-30', 65194.36]
        ]

        revenue_old_data = [
            ['2020-08-03', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-new-30', 40409.55],
            ['2020-08-04', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-30', 64398.69],
            ['2020-08-04', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-new-30', 41550.95],
            ['2020-08-04', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-ret-30', 22843.739999999998],
            ['2020-08-05', 'shipping_city', 'cities', 'Brooklyn', 'Brooklyn', 'revenue-30', 65194.36]
        ]

        c_revenue_new_data = [
            ['2015-08-01', 15, '2020-04-01', 56, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue-pc', -96.90616541353381],
            ['2015-08-01', 15, '2020-05-01', 57, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue', -25602.639999999992],
            ['2015-08-01', 15, '2020-05-01', 57, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue-pc', -96.25052631578944],
            ['2015-09-01', 15, '2017-12-01', 27, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue', 23859.34],
            ['2015-09-01', 15, '2018-01-01', 28, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue', 24161.79]
        ]

        c_revenue_old_data = [
            ['2015-08-01', 15, '2020-04-01', 56, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue-pc',
             -95.90616541353381],
            ['2015-08-01', 15, '2020-05-01', 57, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue',
             -25402.639999999992],
            ['2015-08-01', 15, '2020-05-01', 57, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue-pc',
             -92.25052631578944],
            ['2015-09-01', 15, '2017-12-01', 27, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue',
             21859.34],
            ['2015-09-01', 15, '2018-01-01', 28, 'shipping_city', 'cities', 'New York', 'New York', 'c-revenue',
             24161.79]
        ]

        df_revenue_new = pd.DataFrame(data=revenue_new_data, columns=self.metrics_revenue['columns'])
        df_revenue_old = pd.DataFrame(data=revenue_old_data, columns=self.metrics_revenue['columns'])
        df_c_revenue_new = pd.DataFrame(data=c_revenue_new_data, columns=self.metrics_c_revenue['columns'])
        df_c_revenue_old = pd.DataFrame(data=c_revenue_old_data, columns=self.metrics_c_revenue['columns'])

        csv.create_csv(self.revenue_new_path, df_revenue_new)
        csv.create_csv(self.revenue_old_path, df_revenue_old)
        csv.create_csv(self.c_revenue_new_path, df_c_revenue_new)
        csv.create_csv(self.c_revenue_old_path, df_c_revenue_old)

    def test_diffing_revenue_metric(self):
        result = execute_diffing_task(self.revenue_id, self.metrics_revenue, self.task_id)
        self.assertEqual(result, self.output_file)

    def test_diffing_c_revenue_metric(self):
        result = execute_diffing_task(self.revenue_id, self.metrics_c_revenue, self.task_id)
        self.assertEqual(result, self.output_file)

    def test_diffing_task_invalid_metric(self):
        invalid_metric = 'dummy_metric'
        result = diffing_task(invalid_metric)
        self.assertFalse(result)

    def tearDown(self):
        remove_file(self.revenue_new_path)
        remove_file(self.revenue_old_path)
        remove_file(self.c_revenue_new_path)
        remove_file(self.c_revenue_old_path)
        remove_file(self.output_file)


