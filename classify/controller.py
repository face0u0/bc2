import argparse, tqdm
from classify.entity import DestFile
import sys
from classify.handler.base import provide_handlers
from classify.files import DestWriter, SourceProvider
from pathlib import PurePath

def main():
    parser = argparse.ArgumentParser(description='files classify tool')

    parser.add_argument('path_from', help='path backup from')
    parser.add_argument('path_to', help='path backup to')

    args = parser.parse_args()

    provider = SourceProvider(PurePath(args.path_from))
    writer = DestWriter(PurePath(args.path_to))
    
    for file in tqdm.tqdm(provider.iter(), total=provider.count()):
        handler = provide_handlers(file)
        try:
            dest = handler.convert(file)
            dir = handler.base_dir()
            writer.save(dir/dest.rpath, dest.data)
            del dest.data
        except Exception as e:
            print(f"{file.rpath} export FAILED. \n{e}", file=sys.stderr)
        finally:
            del file.data


