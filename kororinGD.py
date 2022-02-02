
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# サービスアカウントのキーファイルから認証情報を生成する
def CreateCredential(service_account_key):
	return Credentials.from_service_account_file(service_account_key)

# 認証情報からGoogleDriveアクセスのためのサービス生成
def CreateServiceDrive(creds):
	return build("drive", "v3", credentials=creds)

# 作成されたdriveサービス以下のファイルリストを取得する
def FolderList(drive):
	results = drive.files().list(
		q = "mimeType = 'application/vnd.google-apps.folder'",
		fields="files(id,name)").execute()
	items = results.get('files', [])
	dic_file = {}
	for item in items:
		dic_file[item["name"]] = item["id"]
	return dic_file

# driveサービス内にある名前がfolderのフォルダIdを取得する
# なければ-1
def FolderId(drive, folder):
	files = FolderList(drive)
	print(files)
	if folder in files:
		return files[folder]
	else:
		return None

# 指定フォルダ内にファイルが存在しているか確認する
# あったらそのファイルのIDを返す
# なければNone	
def Exists(drive, folder, fname):
	fid = FolderId(drive, folder)
	if fid == -1:
		return None 
	results = drive.files().list(
		q="'"+fid+"' in parents",
		spaces="drive",
		fields="nextPageToken, files(id,name,mimeType,parents)").execute()

	items = results.get('files', [])
	for item in items:
		if item["name"] == fname:
			return item["id"]
	return None 

# 指定フォルダ内にスプレッドシートを作成する
# 成功したらそのシートのIDを返す
# 失敗したらNone
# なお、すでに存在していたらそのシートのIDを返す
def CreateSpreadSheet(drive, folder, sheetname):
	fid = FolderId(drive, folder)
	if fid == -1:
		return None

	check = Exists(drive, folder, sheetname)
	if check:
		return check

	metadata = {
	    'name': sheetname,
	    'parents': [fid],
	    'mimeType': 'application/vnd.google-apps.spreadsheet',
	}
	res = drive.files().create(body=metadata).execute()
	return res["id"]

