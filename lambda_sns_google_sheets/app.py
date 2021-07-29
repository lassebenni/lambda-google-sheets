from lib.utils import extract_messages, read_df_from_s3, add_cols_to_front

import boto3
from sheets.sheet import GoogleSheet

session = boto3.Session(region_name="eu-west-1")


def handler(event, context):
    messages = extract_messages(event)

    bucket = messages['bucket']
    format = messages['format']
    key = messages['key']
    sheet_name = messages['sheet_name']
    worksheet = messages['worksheet']
    ordered_cols = messages['ordered_cols']

    df = read_df_from_s3(bucket, key, format)

    if len(df) > 0:

        df = add_cols_to_front(df, ordered_cols)
        sheet = GoogleSheet(sheet_name)
        sheet.update_sheet(df, worksheet)

        message = f"Succesfully stored dataframe in sheet {sheet_name}"

    else:
        message = "Empty Dataframe. Exiting"

    return {
        "statusCode": 200,
        "body": message
    }
