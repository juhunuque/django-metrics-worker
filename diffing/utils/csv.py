import logging
import pandas as pd

log = logging.getLogger(__name__)


def create_csv(path, df):
    log.info(f'Creating a csv file from a data frame in the path: {path}')
    df.to_csv(path, index=False)
    log.info(f'Created csv file in the path: {path}')
    return path


def load_df(path):
    log.info(f'Loading data frame from the path {path}')
    return pd.read_csv(path)


