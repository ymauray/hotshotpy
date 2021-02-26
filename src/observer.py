from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def start_observer(on_modified):
    patterns = ["[0-9]*_[0-9]*_[0-9]*.png"]
    ignore_patterns = []
    ignore_directories = True
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_modified = on_modified

    path = '/home/yannick/Images'
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    return observer
