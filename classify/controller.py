import argparse, tqdm
import sys
from classify.handler.base import provide_handlers
from classify.files import SourceProvider, save_file
from pathlib import PurePath

def main():
    parser = argparse.ArgumentParser(description='files classify tool')

    parser.add_argument('path_from', help='path backup from')
    parser.add_argument('path_to', help='path backup to')

    args = parser.parse_args()

    path_from = PurePath(args.path_from)
    path_to = PurePath(args.path_to)

    provider = SourceProvider(path_from)
    for file in tqdm.tqdm(provider.iter(), total=provider.count()):
        handler = provide_handlers(file)
        try:
            dest = handler.convert(file)
            dir = handler.save_dir()
            save_file(dest, path_to/dir)
        except Exception:
            print(f"{file.rpath} export FAILED.", file=sys.stderr)


