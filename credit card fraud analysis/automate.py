import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def on_modified(event):
    if event.src_path.endswith('database.db'):
        print("Database modificado. Atualizando gráficos...")
        subprocess.call(['python', 'main.py'])
        print('PDF atualizado!')

        
if __name__ == '__main__':
    event_handler = FileSystemEventHandler()
    event_handler.on_modified = on_modified
    path = 'database'
    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        print("Monitorando")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Fechou")
    observer.join()