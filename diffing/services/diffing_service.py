import logging
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


def diffing_process(**kwargs):
    log.info('Running diffing_process process')
    old_df, new_df = kwargs.get('old_df', None), kwargs.get('new_df', None)
    group_columns = kwargs.get('group_columns', None)
    date_column = kwargs.get('date_column', None)

    # Sorting data frames by date column
    old_df = old_df.sort_values(by=date_column)
    new_df = new_df.sort_values(by=date_column)
    log.info('Sorted data ascending by date')

    # Getting checkpoints to start reducing data frames
    new_df_first_row_date = datetime.strptime(new_df.iloc[0][date_column], '%Y-%m-%d').date()
    new_df_last_row_date = datetime.strptime(new_df.iloc[-1][date_column], '%Y-%m-%d').date()
    old_df_first_row_date = datetime.strptime(old_df.iloc[0][date_column], '%Y-%m-%d').date()
    old_df_last_row_date = datetime.strptime(old_df.iloc[-1][date_column], '%Y-%m-%d').date()

    # Cleaning data frames, excluding dates not present in the other data frame
    df_result = old_df[old_df[date_column].between(str(old_df_first_row_date),
                                                   str(new_df_first_row_date - timedelta(days=1)))]
    old_df = old_df[old_df[date_column].between(str(new_df_first_row_date), str(old_df_last_row_date))]

    df_result = df_result.append(new_df[new_df[date_column].between(str(old_df_last_row_date + timedelta(days=1)),
                                                                    str(new_df_last_row_date))])
    new_df = new_df[new_df[date_column].between(str(new_df_first_row_date), str(old_df_last_row_date))]
    log.info('Excluded dates not present in both data frames')

    # Removing duplicated, since we want to return only rows that are guarantee to have a different values or new ones.
    # Heavy process that can be improved
    df_merged = old_df
    df_merged = df_merged.append(new_df)
    df_merged = df_merged.drop_duplicates()
    log.info('Removed duplicates metrics')

    # Finally grouping and leaving the row that applies for the condition 'value: max'
    df__grouped = df_merged.groupby(group_columns)
    df__grouped = df__grouped.max()
    df__grouped = df__grouped.reset_index()
    df_result = df_result.append(df__grouped)
    log.info('Determined max value for grouped rows')

    return df_result.sort_values(by=date_column)
