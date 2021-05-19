from pathlib import PurePath
from classify.entity import DestFile, SourceFile

class MovieHandler:
    def convert(self, source: SourceFile) -> DestFile:
        updated = source.created
        dirpath = PurePath(updated.strftime("%Y-%m"), source.rpath.name)
        return DestFile(dirpath, source.data)

    def is_in_charge(self, source: SourceFile) -> bool:
        return source.rpath.suffix.lower() in [".mov", ".mp4", ".mkv"]
    
    def save_dir(self) -> PurePath:
        return PurePath("movies")