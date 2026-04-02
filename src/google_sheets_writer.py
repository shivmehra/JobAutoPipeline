# Google Sheets writer
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsWriter:
    def __init__(self, credentials_path, sheet_name):
        self.sheet_name = sheet_name
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, self.scope)
        self.client = gspread.authorize(self.creds)

    def write_data(self, data, worksheet_name='Sheet1'):
        """Write data to Google Sheet"""
        try:
            sheet = self.client.open(self.sheet_name).worksheet(worksheet_name)

            # Clear existing data
            sheet.clear()

            # Prepare headers
            if data:
                headers = list(data[0].keys())
                sheet.append_row(headers)

                # Write data rows
                for item in data:
                    row = [str(item.get(header, '')) for header in headers]
                    sheet.append_row(row)

            print(f"Data written to Google Sheet: {self.sheet_name}")
            return True
        except Exception as e:
            print(f"Error writing to Google Sheets: {e}")
            return False

    def append_data(self, data, worksheet_name='Sheet1'):
        """Append data to existing Google Sheet"""
        try:
            sheet = self.client.open(self.sheet_name).worksheet(worksheet_name)

            if data:
                for item in data:
                    row = [str(value) for value in item.values()]
                    sheet.append_row(row)

            print(f"Data appended to Google Sheet: {self.sheet_name}")
            return True
        except Exception as e:
            print(f"Error appending to Google Sheets: {e}")
            return False</content>
<parameter name="filePath">c:\Shiv\Projects\AIML\JobAutoPipeline\src\google_sheets_writer.py