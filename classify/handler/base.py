from classify.handler.universal import UniversalHandler
from classify.handler.image import ImageHandler
from classify.entity import DestFile, SourceFile

class Handler:
    def convert(self, source: SourceFile) -> DestFile:
        pass

    def isInCharge(self, source: SourceFile) -> bool:
        pass

def provide_handlers(source: SourceFile) -> Handler:
    for handlerT in [ImageHandler]:
        handler: Handler = handlerT()
        if handler.isInCharge(source):
            return handler

    return UniversalHandler()