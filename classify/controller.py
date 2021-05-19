import argparse
from classify.handler.base import provide_handlers
from classify.files import SourceProvider, save_file
from pathlib import PurePath

def main():
    parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')

    parser.add_argument('path_from', help='path backup from')
    parser.add_argument('path_to', help='path backup to')

    args = parser.parse_args()

    path_from = PurePath(args.path_from)
    path_to = PurePath(args.path_to)

    provider = SourceProvider(path_from)
    for file in provider.iter():
        handler = provide_handlers(file)
        dest = handler.convert(file)
        save_file(dest, path_to)

