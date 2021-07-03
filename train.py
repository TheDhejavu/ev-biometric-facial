import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.common.logger import logger
from app.core.facial_recognition import FacialRecognition
import os


def train():
    fr = FacialRecognition()
    cwd = os.getcwd()
    fr.train_images(cwd+"/dataset")
    fr.save_encodings()


class Watcher:
    DIRECTORY_TO_WATCH = "./dataset"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logger.error("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_modified(event):
        print(event)
        if event.is_directory:
            return None
        else:
            train()
            # Taken any action here when a file is modified.
            logger.info(f"Received modified event - {event.src_path}.")


if __name__ == '__main__':
    w = Watcher()
    train()
    w.run()
