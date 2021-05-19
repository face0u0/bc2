import io
import os
import re
import typing
from classify.entity import DestFile, SourceFile
from typing import List, Tuple
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from pathlib import PurePath

class ImageHandler:
    def convert(self, source: SourceFile) -> DestFile:
        img = Image.open(source.data)
        exif = None
        if "exif" in img.info:
            exif = img.info['exif']
        if _compressed_size(img.width, img.height) != None:
            img = img.resize(_compressed_size(img.width, img.height), Image.LANCZOS)
        cimg = io.BytesIO()
        if exif != None:
            img.save(cimg, exif=exif)
        else:
            img.save(cimg)
        return DestFile(_filepath(source), cimg)
    
    def isInCharge(self, source: SourceFile) -> bool:
        return source.rpath.suffix in ["png", "jpeg", "jpg"]

def _exif_date(img: SourceFile) -> datetime:
    exif = Image.open(img.rpath).getexif()
    if 36867 in exif:
        return datetime.datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')
    else:
        return None

def _filepath(file: SourceFile) -> PurePath:
    time = file.created
    if _exif_date(file):
        time = _exif_date(file)
    elif _estimate_created(file):
        time = _estimate_created(file)
    dirname = PurePath("images", time.strftime("%Y-%m"), file.rpath.name)
    return dirname

def _compressed_size(width: int, height: int) -> typing.Tuple[int, int]:
    max_size = 2500*1480
    size = height*width
    if max_size >= size:
        return None
    per = (max_size/size)**0.5
    return (int(width*per), int(height*per))

def _estimate_created(file: os.DirEntry):
    try :
        pattern = re.compile(r'\d+')
        nums = pattern.findall(file.name)
        datesStr = "".join(nums)
        date = None
        if len(datesStr) > 16 or len(datesStr) < 9:
            return None
        elif len(datesStr) == 13:
            date = datetime.datetime.fromtimestamp(int(datesStr[:10]))
        elif len(datesStr) == 14 or len(datesStr) == 16:
            date = datetime.datetime(int(datesStr[:4]), int(datesStr[4:6]), int(datesStr[6:8]))
        else:
            return None
        if date.year <= 2000 or date.year >= 2050:
            return None
        return date
    except Exception:
        return None