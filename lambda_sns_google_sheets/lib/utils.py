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

    if format == 'json':
        return pd.read_json(BytesIO(retr['Body'].read()))
    elif format == 'csv':
        return pd.read_csv(BytesIO(retr['Body'].read()))
        df = pd.read_csv(path)
    elif format == 'feather':
        return pd.read_feather(BytesIO(retr['Body'].read()))
