from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
from .config import load_config
from .extract import extract_text
from .chunk import chunk_text
from .embed import embed_texts
from .store import upsert
from .file_scan import checksum
from .embed import load_model

class JarvisFileHandler(FileSystemEventHandler):
    def __init__(self, cfg):
        self.cfg = cfg
        load_model(cfg["embeddings"]["model"])

    def process(self, file_path: Path):
        if not file_path.is_file():
            return
        if any(file_path.match(pattern) for pattern in self.cfg["ignore"]):
            return
        try:
            text = extract_text(file_path)
            if not text.strip():
                return
            for chunk, start, end in chunk_text(
                text,
                self.cfg["chunk"]["tokens"],
                self.cfg["chunk"]["overlap"]
            ):
                embedding = embed_texts([chunk])[0]
                upsert(
                    [f"{file_path}-{start}-{end}"],
                    [embedding],
                    [{"path": str(file_path), "start": start, "end": end}],
                    [chunk]
                )
            print(f"[green]Indexed: {file_path}[/green]")
        except Exception as e:
            print(f"[red]Failed to index {file_path}: {e}[/red]")

    def on_modified(self, event):
        if not event.is_directory:
            self.process(Path(event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            self.process(Path(event.src_path))

    def on_moved(self, event):
        # Could remove old index entry if desired
        if not event.is_directory:
            self.process(Path(event.dest_path))

def start_watcher():
    cfg = load_config()
    event_handler = JarvisFileHandler(cfg)
    observer = Observer()

    for root in cfg["roots"]:
        path = Path(root).expanduser()
        if path.exists():
            observer.schedule(event_handler, str(path), recursive=True)
            print(f"[cyan]Watching: {path}[/cyan]")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
