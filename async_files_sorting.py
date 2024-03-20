import asyncio
import logging
from argparse import ArgumentParser
from aiopath import AsyncPath
from aioshutil import copyfile


def parse_args_func():
    parser = ArgumentParser()
    parser.add_argument("-s", "--source", help="Source directory", default="test")
    parser.add_argument(
        "-d", "--destination", help="Destination directory", default="dist"
    )

    # parse arguments of command line to get source and destination folder names
    args = parser.parse_args()

    if args.source:
        source_path = AsyncPath(args.source)
        destination_path = AsyncPath(args.destination)
        return source_path, destination_path
    else:
        logging.error("Provide source directory")
        return None


# asynchronously move through folders and files and copy files
async def read_folder(root, dest):
    try:
        if await root.is_dir():
            async for path in root.iterdir():
                await read_folder(path, dest)
        elif await root.is_file():
            await copy_file(root, dest)
        else:
            logging.error(f"Unknown path object {root}")
    except Exception as e:
        logging.error(f"Error while reading folder: {e}")


# asynchronously copy files into subfolders in the dist folder
async def copy_file(file_path, dest_path):
    if await file_path.exists():
        file_name = file_path.name
        file_extension = file_path.suffix.removeprefix(".")
        new_folder_path = AsyncPath(dest_path / file_extension)
        try:
            await new_folder_path.mkdir(exist_ok=True, parents=True)
            await copyfile(file_path, new_folder_path / file_name)
        except OSError as e:
            logging.error(f"Error while copying file: {e}")
        except Exception as e:
            logging.error(f"Ooops, unexpected error: {e}")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    source_path, destination_path = parse_args_func()

    asyncio.run(read_folder(source_path, destination_path))
