from pathlib import PurePath
from classify.entity import DestFile, SourceFile

class UniversalHandler:
    def convert(self, source: SourceFile) -> DestFile:
        updated = source.created
        dirpath = PurePath(updated.strftime("%Y-%m"), source.rpath.name)
        return DestFile(dirpath, source.data)

    def is_in_charge(self, source: SourceFile) -> bool:
        return True

    def base_dir(self) -> PurePath:
        return PurePath("others")