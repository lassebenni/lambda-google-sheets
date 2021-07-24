import json

import pandas as pd


def extract_messages(event: dict):
    try:
        return json.loads(event['Records'][0]['Sns']['Message'])
    except KeyError:
        pass


def read_df_from_s3(path: str, format: str) -> pd.DataFrame:
    df = None

    if format == 'json':
        df = pd.read_json(path)
    elif format == 'csv':
        df = pd.read_csv(path)
    elif format == 'feather':
        df = pd.read_feather(path)

    return df
