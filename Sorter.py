import argparse
import shutil
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

print(parser.parse_args())
args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []

FILE_EXTENSIONS = {
    'images': {'jpeg', 'png', 'jpg', 'svg'},
    'video': {'avi', 'mp4', 'mov', 'mkv'},
    'documents': {'doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'},
    'audio': {'mp3', 'ogg', 'wav', 'amr'},
    'archives': {'zip', 'gz', 'tar'}
}


def get_name_dir(ex: Path) -> str:
    name_dir = ""
    for key, val in FILE_EXTENSIONS.items():
        if ex.suffix[1:] in val:
            name_dir = key
            break
    if not name_dir:  # якщо немає співпадіння
        name_dir = "others"
    return name_dir


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            if ext not in FILE_EXTENSIONS.get("archives"):
                ext_folder = output / get_name_dir(el) / ext
                try:
                    ext_folder.mkdir(exist_ok=True, parents=True)
                    copyfile(el, ext_folder / el.name)
                except OSError as err:
                    logging.error(err)
            else:
                ext_folder = output / "archives"
                try:
                    ext_folder.mkdir(exist_ok=True, parents=True)
                    copyfile(el, ext_folder / el.name)
                except OSError as err:
                    logging.error(err)


def extract_archive(archive_path: Path, del_archive=True):
    """
    Extract the contents of an archive file to a target directory.

    Args:
        archive_path (Path): The path to the archive file.
        del_archive (bool, optional): Whether to delete the archive file after extraction. Defaults to True.
    """
    target_dir = archive_path.parent / archive_path.stem  # шлях до папки з іменем архіву
    target_dir.mkdir(exist_ok=True)  # папка для архіву
    try:
        shutil.unpack_archive(archive_path, target_dir)  # розпаковка
        if del_archive:  # видалення архіву
            archive_path.unlink()
    except ValueError:
        print(f"Failed to unpack the archive: {archive_path.name}")
    except shutil.ReadError:
        print(f"Archive - {archive_path.stem} not unpacked\tunknown extension({archive_path.suffix})")


def worker_archives():
    zip_folder = Path(output).resolve().parent / output / 'archives'  # Шлях до папки 'archives'

    if zip_folder.exists() and zip_folder.is_dir():  # Перевіряємо, чи існує та є папкою
        for archive_path in zip_folder.iterdir():  # Отримуємо список файлів у папці 'zip'
            if archive_path.is_file():
                extract_archive(archive_path)  # Викликаємо функцію розпаковки архіву


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(threadName)s %(message)s')

    folders.append(source)
    grabs_folder(source)
    print(folders)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    worker_archives()

    print(f'Можна видалити {source}')
