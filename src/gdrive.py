"""
This module is a wrapper for google drive api
"""
from googleapiclient.discovery import build
from google_auth import creds

service = build('drive', 'v3', credentials=creds)

def get_sheet_id(name):
    """
    returns the Id of the given spread sheet
    Args:
        `name`:string - name of the spreadsheet
    Returns: Id of the spreadsheet
    """
    result = service.files().list(q=f"name='{name}'", pageSize=10, fields="nextPageToken, files(id, name)").execute()
    return '' if not result['files'] else result['files'][0]['id']
