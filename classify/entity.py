from datetime import datetime
from io import BytesIO
import pathlib
from dataclasses import dataclass

@dataclass
class SourceFile:
    # represents relative path
    rpath: pathlib.PurePath
    created: datetime  # created timestamp
    data: BytesIO

@dataclass
class DestFile:
    # represents relative path
    rpath: pathlib.PurePath
    data: BytesIO
