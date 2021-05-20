from datetime import datetime
import hashlib
from io import BytesIO
import os
from classify.entity import DestFile, SourceFile
import pathlib
from typing import Generator, List, NoReturn

def _scan_tree(path: pathlib.PurePath) -> List[os.DirEntry]:
    result = []
    files = list(os.scandir(path))
    result.extend(files)
    for file in files:
        if file.is_dir():
            result.extend(_scan_tree(file.path))
    return result

def _sha256(io: BytesIO) -> str:
    return hashlib.sha256(io.getvalue()).hexdigest()

class SourceProvider:

    def __init__(self, base: pathlib.PurePath):
        self._base = base
        self._entries = list(filter(lambda f: f.is_file(), _scan_tree(base)))

    def count(self) -> int:
        return len(self._entries)

    def iter(self) -> Generator[SourceFile, NoReturn, NoReturn]:
        for file in self._entries:
            rpath = pathlib.PurePath(file.path).relative_to(self._base) # 相対パスに変換
            created = datetime.fromtimestamp(file.stat().st_ctime)
            with open(file.path, "rb") as f:
                io = BytesIO(f.read())
                yield SourceFile(rpath, created, io)

class DestWriter:

    def __init__(self, base: pathlib.PurePath):
        self._base = base

    def save(self, rpath: pathlib.PurePath, data: BytesIO):
        path = self._base / rpath
        if os.path.exists(path):
            with open(path, 'rb') as f:
                if _sha256(BytesIO(f.read())) == _sha256(data):
                    return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.getvalue())
        

