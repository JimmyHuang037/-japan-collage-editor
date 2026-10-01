"""Download only screened candidates, keeping ID filenames and verifying Drive MD5."""
import hashlib
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from googleapiclient.http import MediaIoBaseDownload
from drive import service, ROOT


def main():
    candidates = json.loads((ROOT / 'data/screening/candidates.json').read_text())
    inventory = {r['id']: r for r in json.loads((ROOT / 'data/reference/drive-current.json').read_text())}
    thread = threading.local()
    def get(row):
        info = inventory[row['id']]
        path = ROOT / 'data/originals' / (row['id'] + '.jpg')
        if path.exists():
            if info.get('md5Checksum') and hashlib.md5(path.read_bytes()).hexdigest() != info['md5Checksum']:
                raise RuntimeError('Existing original differs: ' + row['id'])
            return 'existing'
        if not hasattr(thread, 'api'):
            thread.api = service()
        part = path.with_suffix('.part')
        with part.open('wb') as stream:
            download = MediaIoBaseDownload(stream, thread.api.files().get_media(fileId=row['id']), chunksize=4 * 1024 * 1024)
            done = False
            while not done:
                _, done = download.next_chunk(num_retries=3)
        raw = part.read_bytes()
        if not info.get('md5Checksum') or hashlib.md5(raw).hexdigest() != info['md5Checksum']:
            part.unlink()
            raise RuntimeError('MD5 mismatch: ' + row['id'])
        part.replace(path)
        return 'downloaded'
    with ThreadPoolExecutor(max_workers=4) as pool:
        tasks = {pool.submit(get, row): row for row in candidates}
        for i, task in enumerate(as_completed(tasks), 1):
            row = tasks[task]
            try:
                print(f"Candidate {row['number']:04d}: {task.result()} ({i}/{len(tasks)})", flush=True)
            except Exception as exc:
                print('Candidate download failed: ' + type(exc).__name__, flush=True)
                raise SystemExit(1)


if __name__ == '__main__':
    main()
