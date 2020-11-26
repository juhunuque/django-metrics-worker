REVENUE_CSV = dict(
    old='revenue_old.csv',
    new='revenue_new.csv',
    dtypes={
        'date': 'category',
        'segment_field': 'category',
        'segment_name': 'category',
        'segment_value': 'category',
        'segment_value_id': 'category',
        'stat': 'category',
        'value': 'category',
    },
    group_columns=['date', 'segment_field', 'segment_value_id', 'stat'],
    columns=['date', 'segment_field', 'segment_name', 'segment_value', 'segment_value_id', 'stat', 'value'],
    date_column='date'
)


REVENUE_CSV_TEST = dict(
    old='revenue_old_test.csv',
    new='revenue_new_test.csv',
    dtypes={
        'date': 'category',
        'segment_field': 'category',
        'segment_name': 'category',
        'segment_value': 'category',
        'segment_value_id': 'category',
        'stat': 'category',
        'value': 'category',
    },
    group_columns=['date', 'segment_field', 'segment_value_id', 'stat'],
    columns=['date', 'segment_field', 'segment_name', 'segment_value', 'segment_value_id', 'stat', 'value'],
    date_column='date'
)


C_REVENUE_CSV = dict(
    old='c_revenue_old.csv',
    new='c_revenue_new.csv',
    dtypes={
        'cohort': 'category',
        'cohort_id': 'category',
        'month_date': 'category',
        'month_nth': 'category',
        'segment_field': 'category',
        'segment_name': 'category',
        'segment_value': 'category',
        'segment_value_id': 'category',
        'stat': 'category',
        'value': 'category',
    },
    group_columns=['cohort', 'cohort_id', 'month_nth', 'segment_field', 'segment_value_id', 'stat'],
    columns=['cohort', 'cohort_id', 'month_date', 'month_nth', 'segment_field', 'segment_name', 'segment_value',
             'segment_value_id', 'stat', 'value'],
    date_column='cohort'
)


C_REVENUE_CSV_TEST = dict(
    old='c_revenue_old_test.csv',
    new='c_revenue_new_test.csv',
    dtypes={
        'cohort': 'category',
        'cohort_id': 'category',
        'month_date': 'category',
        'month_nth': 'category',
        'segment_field': 'category',
        'segment_name': 'category',
        'segment_value': 'category',
        'segment_value_id': 'category',
        'stat': 'category',
        'value': 'category',
    },
    group_columns=['cohort', 'cohort_id', 'month_nth', 'segment_field', 'segment_value_id', 'stat'],
    columns=['cohort', 'cohort_id', 'month_date', 'month_nth', 'segment_field', 'segment_name', 'segment_value',
             'segment_value_id', 'stat', 'value'],
    date_column='cohort'
)

METRIC_CSV = dict(
    revenue=REVENUE_CSV,
    c_revenue=C_REVENUE_CSV,
    cohort_revenue=C_REVENUE_CSV
)

METRIC_CSV_TEST = dict(
    revenue=REVENUE_CSV_TEST,
    c_revenue=C_REVENUE_CSV_TEST,
    cohort_revenue=C_REVENUE_CSV_TEST
)