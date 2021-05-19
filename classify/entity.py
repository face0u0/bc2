from datetime import datetime
from io import BytesIO
import pathlib
from dataclasses import dataclass

@dataclass
class SourceFile:
    path: pathlib.PurePath # .name, .suffix, .stem ...etc
    created: datetime  # created timestamp
    data: BytesIO

@dataclass
class DestFile:
    rpath: pathlib.PurePath # represents relative path
    data: BytesIO
