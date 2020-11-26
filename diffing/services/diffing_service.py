import logging
import pandas as pd

log = logging.getLogger(__name__)


def diffing_process(**kwargs):
    log.info('Running diffing_process process')
    old_df, new_df = kwargs.get('old_df', None), kwargs.get('new_df', None)
    group_columns = kwargs.get('group_columns', None)
    columns = kwargs.get('columns', None)

    # Merging both data frames and removing duplicates. Notice we specify which columns we want to evaluate and obtain
    # what is duplicated. Duplicates are removed from the result
    df_result = pd.concat([old_df, new_df], ignore_index=True)\
        .drop_duplicates(subset=columns, keep=False)\
        .reset_index(drop=True)
    log.info('Data frames merged and removed duplicates metrics')

    # Finally grouping and leaving the row that applies for the condition 'value: max'
    df_result = df_result.groupby(group_columns, sort=False).max().reset_index()
    log.info('Determined max value for grouped rows')

    return df_result
