import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class Watcher:
    DIRECTORY_TO_WATCH = "C:/Users/Utilities99/Pictures/consumos"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def process(event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.src_path
            path to the changed file
        """
        if event.event_type == 'modified':
            print(f"Received modified event - {event.src_path}")
            copy_file(event.src_path)

    def on_modified(self, event):
        self.process(event)

def copy_file(src_path):
    # Ruta del directorio de destino dentro del proyecto
    dst_path = os.path.join('C:/Users/Utilities99/Documents/territorioSeguro/ultimo2', 'static', 'images')  # Actualiza esta ruta a tu carpeta del proyecto
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    shutil.copy(src_path, dst_path)

def start_watcher():
    w = Watcher()
    w.run()

def upload_to_github():
    while True:
        time.sleep(60)  # Verificar cada 60 segundos
        os.system("git add .")
        os.system('git commit -m "Auto-update images"')
        os.system("git push")

if __name__ == '__main__':
    watcher_thread = threading.Thread(target=start_watcher)
    github_thread = threading.Thread(target=upload_to_github)

    watcher_thread.start()
    github_thread.start()

    watcher_thread.join()
    github_thread.join()
