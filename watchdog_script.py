import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print("Detected change in script, restarting...")
            os.execv(sys.executable, ['python'] + [self.script])

if __name__ == "__main__":
    script = 'bot.py'
    event_handler = RestartHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        os.system(f'python {script}')
    except KeyboardInterrupt:
        observer.stop()
    observer.join()