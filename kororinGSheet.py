# -*- coding: utf-8 -*-

from googleapiclient.discovery import build

# 認証情報からGoogleDriveアクセスのためのサービス生成
def Service(creds):
	return build("sheets", "v4", credentials=creds)

def Clear(service, spreadsheet_id, sheetname):
    return service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, body={}, range=sheetname).execute()

def Update(service, spreadsheet_id, sheetname, values):
    data = [
        {
            'range' : sheetname,
            'values': values
        },
    ]

    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }

    return service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()

def SortTabs(service, spreadsheet_id, is_asc=True):
    response = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets   = response["sheets"]
    names    = []
    for s in sheets:
        names.append(s["properties"]["title"])

    if is_asc:
        names.sort(reverse=False)
    else:
        names.sort(reverse=True)

    requests = []
    for s in sheets:
        idx = names.index(s["properties"]["title"])
        s["properties"]["index"] = idx
        requests.append({
            "updateSheetProperties": {
                "properties": s["properties"],
                "fields": "*"
            }
        })

    request_body = {"requests": requests} 
    return service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body = request_body 
    ).execute()


