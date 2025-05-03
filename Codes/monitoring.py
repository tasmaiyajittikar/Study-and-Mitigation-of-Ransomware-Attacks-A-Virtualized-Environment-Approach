from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
class MonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"[ALERT] File modified: {event.src_path}")
def on_created(self, event):
        print(f"[INFO] New file created: {event.src_path}")
if __name__ == "__main__":
    path = "critical"  # Directory to monitor
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
