import os

from gspread_pandas import Spread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

client_email = os.getenv('GOOGLE_CLIENT_EMAIL', '')
client_id = os.getenv('GOOGLE_CLIENT_ID', '')
private_key = os.getenv('GOOGLE_PRIVATE_KEY', '').replace('\\n', '\n')
private_key_id = os.getenv('GOOGLE_PRIVATE_KEY_ID', '')
project_id = os.getenv('GOOGLE_PROJECT_ID', '')

creds_dict = {
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "client_email": client_email,
    "client_id": client_id,
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service%40sheets-scraper-302209.iam.gserviceaccount.com",
    "private_key_id": private_key_id,
    "private_key": private_key,
    "token_uri": "https://oauth2.googleapis.com/token",
    "type": "service_account",
}


class GoogleSheet():
    spread = None
    sheet_name = None

    def __init__(self, sheet_name):
        credentials = self.get_credentials()
        self.spread = Spread(sheet_name, creds=credentials)

    def get_credentials(self):
        return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    def update_sheet(self, df, worksheet_name, replace_sheet: bool = False):
        self.spread.df_to_sheet(df, index=False, sheet=worksheet_name,
                                start='A1', replace=replace_sheet)
