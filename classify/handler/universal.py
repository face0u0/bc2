from pathlib import PurePath
from classify.entity import DestFile, SourceFile

class UniversalHandler:
    def convert(self, source: SourceFile) -> DestFile:
        updated = source.created
        dirpath = PurePath("others", updated.strftime("%Y-%m"), source.path.name)
        return DestFile(dirpath, source.data)

    def isInCharge(self, source: SourceFile) -> bool:
        return True