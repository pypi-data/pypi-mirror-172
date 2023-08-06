#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from umnet_scripts import cyberark


class GoogleSheet(object):
    def __init__(self):
        cyberark = Cyberark("UMNET")
        self.scope_app = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.service_account_email = str(cyberark.query_cyberark("gsheet_api_service_account_email"))
        self.project_id = str(cyberark.query_cyberark("gsheet_api_project_id"))
        self.client_id = str(cyberark.query_cyberark("gsheet_api_client_id"))
        self.private_key_id = str(cyberark.query_cyberark("gsheet_api_key_id"))
        self.private_key = str(cyberark.query_cyberark("gsheet_api_private_key")).replace("\\n", "\n")

    def _gsheet_auth(self):
        json_creds = {
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.service_account_email,
            "client_id": self.client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/" + self.service_account_email.replace("@", "%40"),
        }
        cred = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, self.scope_app)

        # authorize the clientsheet
        return gspread.authorize(cred)

    def open_google_sheet(self, sheet_id, sheet_num):
        client = self._gsheet_auth()
        sheet = client.open_by_key(sheet_id)

        sheet_instance = sheet.get_worksheet(sheet_num)

        # return a list of dictionaries.  Each list entry is a row, with the keys being the column headers
        return sheet_instance.get_all_records()
