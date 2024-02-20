from os import scandir, rename
import watchdog
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# folder to track e.g. Windows: "C:\\Users\\User\\Downloads"
source_dir = "C:\\Users\\User\\Downloads"
dest_dir_music = "C:\\Users\\User\\Downloads\\music"
dest_dir_video = "C:\\Users\\User\\Downloads\\video"
dest_dir_image = "C:\\Users\\User\\Downloads\\image"
dest_dir_documents = "C:\\Users\\User\\Downloads\\documents"
dest_dir_application = "C:\\Users\\User\\Downloads\\application"
dest_dir_zip = "C:\\Users\\User\\Downloads\\zip"


# supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".png", ".gif", ".webp",
                    ".bmp", ".jpf", ".jpx", ".jpm",".svg"]
# supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".qt", ".flv"]
# upported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# supported Document types
document_extensions = [".doc", ".docx", ".html",".odt",
                       ".pdf", ".xls", ".xlsx", ".csv",".ppt", ".pptx", ".ipynb"]
# supported Application types
application_extentions = [".exe", ".msi"]
# supported Zip types
zip_extensions = ['.zip']


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_application_files(entry, name)
                self.check_zip_files(entry, name)


    def check_audio_files(self, entry, name):  # Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")
            
    def check_application_files(self, entry, name): # Checks all Application Files
        for application_extension in application_extentions:
            if name.endswith(application_extension) or name.endswith(application_extension.upper()):
                move_file(dest_dir_application, entry, name)
                logging.info(f"Moved application file: {name}")

    def check_zip_files(self, entry, name): # Checks all zip Files
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                move_file(dest_dir_zip, entry, name)
                logging.info(f"Moved zip file : {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    