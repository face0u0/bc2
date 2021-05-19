#!/usr/bin/python3
import os, datetime, shutil, hashlib, sys, re
import tqdm
from typing import List, Tuple
from PIL import Image
from PIL.ExifTags import TAGS

if len(sys.argv) != 3:
    print('Error: filepath not detected.', file=sys.stderr)
    exit(1)
FROM = sys.argv[1]
TO = sys.argv[2]
IMAGES = ["png", "jpeg", "jpg"]

def scan_tree(path: str) -> List[os.DirEntry]:
    result = []
    files = list(os.scandir(path))
    result.extend(files)
    for file in files:
        if file.is_dir():
            result.extend(scan_tree(file.path))
    return result

def extention(file: os.DirEntry):
    _, file_extension = os.path.splitext(file.name)
    return file_extension[1:].lower()

def sha256(path: str):
    with open(path,'rb') as f:
        checksum = hashlib.sha256(f.read()).hexdigest()
        return checksum

def copy_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        if sha256(src) != sha256(dest):
            # log if already exist in dest, and may not samefile. 
            print(f"{src} ----> {dest} FAILED!")
    else:
        shutil.copy2(src, dest)

def estimate_created(file: os.DirEntry):
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

class ImageHandler:
    def classify(self, file: os.DirEntry):
        dirname = self.filepath(file)
        os.makedirs(os.path.dirname(dirname), exist_ok=True)
        img = Image.open(file.path)
        exif = None
        if "exif" in img.info:
            exif = img.info['exif']
        if ImageHandler.compressed_size(img.width, img.height) != None:
            img = img.resize(ImageHandler.compressed_size(img.width, img.height), Image.LANCZOS)
        if exif != None:
            img.save(dirname, exif=exif)
        else:
            img.save(dirname)
    
    def filepath(self, file: os.DirEntry):
        time = datetime.datetime.fromtimestamp(file.stat().st_ctime)
        if ImageHandler.exif_date(file):
            time = ImageHandler.exif_date(file)
        elif estimate_created(file):
            time = estimate_created(file)
        dirname = os.path.join(TO, "images", time.strftime("%Y-%m"), file.name)
        return dirname

    @staticmethod
    def compressed_size(width: int, height: int) -> Tuple(int, int):
        max_size = 2500*1480
        size = height*width
        if max_size >= size:
            return None
        per = (max_size/size)**0.5
        return (int(width*per), int(height*per))
    
    @staticmethod
    def exif_date(img: os.DirEntry) -> datetime.datetime:
        exif = Image.open(img.path).getexif()
        if 36867 in exif:
            return datetime.datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')
        else:
            return None

class UniversalHandler:
    def classify(self, file: os.DirEntry):
        updated = datetime.datetime.fromtimestamp(file.stat().st_ctime)
        dirname = os.path.join(TO, "others", updated.strftime("%Y-%m"), file.name)
        copy_file(file.path, dirname)

files = scan_tree(FROM)

for file in tqdm.tqdm(files):
    if file.is_file():
        filetype = extention(file) 
        hendler = UniversalHandler()       
        if filetype in IMAGES:
            hendler = ImageHandler()
        hendler.classify(file)
            