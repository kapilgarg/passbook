"""
This module is a wrapper for google sheet api
"""
from googleapiclient.discovery import build
from google_auth import creds

service = build('sheets', 'v4', credentials=creds)


def create_spreadsheet(name):
    """
    creates a spread sheet with the given name
    """
    spreadsheet_body = {
        'properties': {
            'title': name
        }
    }
    spreadsheet = service\
        .spreadsheets()\
        .create(body=spreadsheet_body, fields='spreadsheetId')\
        .execute()
    return spreadsheet.get('spreadsheetId')

def add_sheet(spreadsheet_id, sheet_name):
    """
    Adds a sheet to an existing spreadsheet
    Args:
        spreadsheet_id:string - Id of the spreadsheet
        sheet_name:string - name of the sheet to be added    
    """
    batch_update_spreadsheet_request_body = {
        'requests': [
            {'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }}
        ]}
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body)
    try:
        request.execute()
    except Exception as ex:
         if ex.content.decode('utf-8').index(f'A sheet with the name \\"{sheet_name}\\" already exists')!= -1:
            #clear_sheet(spreadsheet_id, sheet_name)
            pass

def create_spread_sheet(name):
    """
    creates a spread sheet with the given name
    Args:
        name:string - name of the spreadsheet
    Returns: spreatsheet Id
    """
    spreadsheet = {
        'properties': {
            'title': name
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')

def clear_sheet(spreadsheet_id, sheet):    
    """
    clears all the data from a sheet in a spreadsheet
    Args:
        spreadsheet_id:string - Id of the spreadsheet
    """
    range_name = f"{sheet}"
    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name)
    request.execute()

def write_to_sheet(spreadsheet_id, sheet, values):
    """
    writes values to a sheet in spreadsheet
    Args:
        spreadsheet_id:string - Id of the spreadsheet
        sheet:string - name of the sheet
        body:list - list of values to be written
    """
    body = {
            'values': values
        }
    range_name = f"{sheet}"
    service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="RAW", body=body).execute()

def get_from_sheet(spreadsheet_id, sheet_name):
    """
    reads the data from a sheet
    Args:
        spreadsheet_id:string - Id of the spreadsheet
        sheet:string - name of the sheet
    """
    range_name = f"{sheet_name}"
    data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return data['values'] if data else None

def de_duplicate(spreadsheet_id, sheet_name):
    values = get_from_sheet(spreadsheet_id, sheet_name)
    final_values = []
    id_map = {}
    for value in values:
        if(value[5] not in id_map):
            id_map[value[5]] = 'true'
            final_values.append(value)
    if final_values:
        clear_sheet(spreadsheet_id, sheet_name)
        write_to_sheet(spreadsheet_id, sheet_name, final_values)
    


