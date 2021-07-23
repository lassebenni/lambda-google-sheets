import json

import pandas as pd
import boto3
from sheets.sheet import GoogleSheet

session = boto3.Session(region_name="eu-west-1")


def handler(event, context):
    messages = extract_messages(event)
    print(messages)

    s3_path = messages['s3_path']
    sheet_name = messages['sheet_name']
    worksheet = messages['worksheet']

    df = pd.DataFrame(columns=[], rows=[])

    if len(df) > 0:
        sheet = GoogleSheet(sheet_name)
        sheet.update_sheet(df, 's3')

        message = f"Succesfully stored dataframe in sheet {sheet_name}"

    else:
        message = "Empty Dataframe. Exiting"

    return {
        "statusCode": 200,
        "body": message
    }


def extract_messages(event: dict):
    try:
        return json.loads(event['Records'][0]['Sns']['Message'])
    except KeyError:
        pass
