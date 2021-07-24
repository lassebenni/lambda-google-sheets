from lib.utils import extract_messages, read_df_from_s3

import boto3
from sheets.sheet import GoogleSheet

session = boto3.Session(region_name="eu-west-1")

def handler(event, context):
    messages = extract_messages(event)

    s3_path = messages['s3_path']
    format = messages['format']

    df = read_df_from_s3(s3_path, format)

    if len(df) > 0:
        sheet_name = messages['sheet_name']
        worksheet = messages['worksheet']

        sheet = GoogleSheet(sheet_name)
        sheet.update_sheet(df, worksheet)

        message = f"Succesfully stored dataframe in sheet {sheet_name}"

    else:
        message = "Empty Dataframe. Exiting"

    return {
        "statusCode": 200,
        "body": message
    }
