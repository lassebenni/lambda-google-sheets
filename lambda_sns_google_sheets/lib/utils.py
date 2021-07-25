from io import BytesIO
import json

import pandas as pd
import boto3

s3 = boto3.client('s3')


def extract_messages(event: dict):
    try:
        return json.loads(event['Records'][0]['Sns']['Message'])
    except KeyError:
        pass


def read_df_from_s3(bucket: str, key: str, format: str) -> pd.DataFrame:
    retr = s3.get_object(Bucket=bucket, Key=key)
    body_as_bytes = BytesIO(retr['Body'].read())

    if format == 'json':
        return pd.read_json(body_as_bytes)
    elif format == 'parquet':
        return pd.read_parquet(body_as_bytes)
    elif format == 'csv':
        return pd.read_csv(body_as_bytes)
        df = pd.read_csv(path)
    elif format == 'feather':
        return pd.read_feather(body_as_bytes)
