from classify.handler.movie import MovieHandler
from pathlib import PurePath
from classify.handler.universal import UniversalHandler
from classify.handler.image import ImageHandler
from classify.entity import DestFile, SourceFile

class Handler:
    def convert(self, source: SourceFile) -> DestFile:
        pass

    def is_in_charge(self, source: SourceFile) -> bool:
        pass

    def save_dir(self) -> PurePath:
        pass

def provide_handlers(source: SourceFile) -> Handler:
    for handlerT in [MovieHandler, ImageHandler]:
        handler: Handler = handlerT()
        if handler.is_in_charge(source):
            return handler

    return UniversalHandler()