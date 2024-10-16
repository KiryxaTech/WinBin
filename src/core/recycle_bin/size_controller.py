from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class SizeHandler(FileSystemEventHandler):
    def __init__(self, action):
        super().__init__()
        self.__action = action

    def on_modified(self, event):
        print(f'Изменение в корзине: {event.src_path}')
        self.__action()


class SizeController:
    def __init__(self, action: callable) -> None:
        self.__action = action
        self.__tracking = False
        self.__observer = Observer()

    def start_tracking(self) -> None:
        if not self.__tracking:
            event_handler = SizeHandler(self.__action)
            self.__observer.schedule(event_handler, path='C:/$Recycle.Bin', recursive=False)
            self.__observer.start()
            self.__tracking = True

    def stop_tracking(self) -> None:
        """Останавливает отслеживание изменений."""
        if self.__tracking:
            self.__observer.stop()
            self.__observer.join()
            self.__tracking = False