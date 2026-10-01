"""Local-only, readonly Drive access. Credentials never enter the web workspace."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER = '17OR9nBcx1xC9-1_FMy6UGngP0rHlSQ9d'
SECRETS = Path('/credentials')
ROOT = Path('/app')


def save_token(creds):
    path = SECRETS / 'token.json'
    temp = path.with_suffix('.tmp')
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        f.write(creds.to_json())
    temp.replace(path)
    path.chmod(0o600)


def credentials():
    path = SECRETS / 'token.json'
    if not path.exists():
        raise RuntimeError('尚未授权：先放置 client.json，再执行 auth。')
    creds = Credentials.from_authorized_user_file(path, SCOPES)
    if not creds.valid:
        if not creds.refresh_token:
            raise RuntimeError('缺少刷新令牌，需要重新执行 auth。')
        creds.refresh(Request())
        save_token(creds)
    return creds


def auth():
    config = SECRETS / 'client.json'
    if not config.exists():
        raise RuntimeError('请将桌面应用客户端 JSON 放到 ~/.config/japan-collage/client.json。')
    if 'installed' not in json.loads(config.read_text()):
        raise RuntimeError('客户端必须是 Desktop app 类型。')
    flow = InstalledAppFlow.from_client_secrets_file(config, SCOPES, autogenerate_code_verifier=True)
    creds = flow.run_local_server(host='127.0.0.1', bind_addr='0.0.0.0', port=8765, open_browser=False,
        access_type='offline', prompt='consent', timeout_seconds=900,
        authorization_prompt_message='在浏览器打开此授权地址：\n{url}',
        success_message='授权完成，可以关闭此页并返回 Codex。')
    if not creds.refresh_token:
        raise RuntimeError('Google 未签发刷新令牌，请重新授权。')
    save_token(creds)
    print('授权已保存；包含刷新令牌。正在检查目标文件夹。')
    check()


def service():
    return build('drive', 'v3', credentials=credentials(), cache_discovery=False)


def check():
    api = service()
    folder = api.files().get(fileId=FOLDER, fields='id,name,mimeType').execute()
    files = api.files().list(q=f"'{FOLDER}' in parents and trashed=false", pageSize=1,
        fields='files(id,name),nextPageToken').execute()
    print(json.dumps({'authenticated': True, 'refresh_token': bool(credentials().refresh_token),
        'folder': folder, 'can_list': True, 'sample_count': len(files.get('files', []))}, ensure_ascii=False))


def sync(limit):
    api = service()
    pending = [FOLDER]
    rows = []
    while pending:
        parent = pending.pop()
        token = None
        while True:
            page = api.files().list(q=f"'{parent}' in parents and trashed=false", pageSize=1000,
                pageToken=token, fields='nextPageToken,files(id,name,mimeType,size,md5Checksum,modifiedTime,imageMediaMetadata,capabilities/canDownload)').execute()
            for row in page.get('files', []):
                if row['mimeType'] == 'application/vnd.google-apps.folder':
                    pending.append(row['id'])
                elif row['mimeType'].startswith('image/'):
                    rows.append(row)
            token = page.get('nextPageToken')
            if not token:
                break
    out = ROOT / 'data/reference/drive-current.json'
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    downloaded = 0
    for row in rows:
        target = ROOT / 'data/originals' / (row['id'] + '.jpg')
        if target.exists() and (not row.get('md5Checksum') or hashlib.md5(target.read_bytes()).hexdigest() == row['md5Checksum']):
            continue
        if limit and downloaded >= limit:
            break
        if not row.get('capabilities', {}).get('canDownload', False):
            continue
        if target.exists():
            raise RuntimeError(f"原片版本变化，保留已有文件等待处理：{row['id']}")
        part = target.with_suffix('.part')
        with part.open('wb') as f:
            download = MediaIoBaseDownload(f, api.files().get_media(fileId=row['id']), chunksize=4 * 1024 * 1024)
            done = False
            while not done:
                _, done = download.next_chunk(num_retries=3)
        if row.get('md5Checksum') and hashlib.md5(part.read_bytes()).hexdigest() != row['md5Checksum']:
            part.unlink()
            raise RuntimeError('下载校验失败：' + row['id'])
        part.replace(target)
        downloaded += 1
        print(f"下载 {downloaded}: {row['id']}", flush=True)
    print(json.dumps({'inventory': len(rows), 'downloaded': downloaded}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['auth', 'check', 'sync'])
    parser.add_argument('--limit', type=int, default=0, help='0 downloads all missing originals')
    args = parser.parse_args()
    try:
        {'auth': auth, 'check': check, 'sync': lambda: sync(args.limit)}[args.command]()
    except Exception as exc:
        # Never dump an exception containing OAuth request URLs or token payloads.
        if isinstance(exc, RuntimeError): print(str(exc))
        else: print('Drive 操作失败：' + type(exc).__name__ + '；检查网络、客户端状态或重新授权。')
        raise SystemExit(1)
