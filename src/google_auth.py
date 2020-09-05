"""
This module sets the google credentials for accessing the services.
"""
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

def __set_credential():
    google_creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            google_creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not google_creds or not google_creds.valid:
        if google_creds and google_creds.expired and google_creds.refresh_token:
            google_creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            google_creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(google_creds, token)
    return google_creds

creds = __set_credential()
