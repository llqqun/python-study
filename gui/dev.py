import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            print(f"检测到更改: {event.src_path}，重启应用...")
            self.start_process()

if __name__ == "__main__":
    script = "gui/main.py"  # 你的主程序路径
    event_handler = ReloadHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path="gui", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()