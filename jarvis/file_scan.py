# ...existing code...
from pathlib import Path
import fnmatch, os, hashlib

def iter_files(roots, ignore_globs):
    for root in roots:
        root = Path(os.path.expanduser(root))
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            rel = str(p)
            if any(fnmatch.fnmatch(rel, pat) for pat in ignore_globs):
                continue
            yield p

def checksum(p: Path):
    h = hashlib.sha1()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
