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