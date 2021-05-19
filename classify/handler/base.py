from classify.handler.movie import MovieHandler
from pathlib import PurePath
from classify.handler.universal import UniversalHandler
from classify.handler.image import ImageHandler
from classify.entity import DestFile, SourceFile

class Handler:
    # ファイル名と中身（画像なら圧縮とか）を変換する
    def convert(self, source: SourceFile) -> DestFile:
        pass

    # 自身が担当のファイル形式ならtrue
    def is_in_charge(self, source: SourceFile) -> bool:
        pass

    # 保存先ディレクトリのベース部分を返す（画像なら"images/"とか）
    def save_dir(self) -> PurePath:
        pass

def provide_handlers(source: SourceFile) -> Handler:
    for handlerT in [MovieHandler, ImageHandler]:
        handler: Handler = handlerT()
        if handler.is_in_charge(source):
            return handler

    return UniversalHandler()