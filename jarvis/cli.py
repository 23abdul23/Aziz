# ...existing code...
import typer
from rich import print
from .config import load_config
from .file_scan import iter_files
from .embed import load_model
from .retrieve import search
from .file_scan import iter_files, checksum
from .extract import extract_text
from .chunk import chunk_text
from .embed import embed_texts
from .store import upsert, reset_collection
from .watcher import start_watcher
from .llm import run_llm

app = typer.Typer()


@app.command()
def watch():
    """Run Jarvis in always-on mode (auto-index changes)"""
    start_watcher()
    
@app.command()
def index(full: bool = False):
    cfg = load_config()
    load_model(cfg["embeddings"]["model"])
    # reset_collection()  # Clear the vector DB before indexing
    
    for file_path in iter_files(cfg["roots"], cfg["ignore"]):
        text = extract_text(file_path)
        print(text, "\n")

        if not text.strip():
            continue
        for chunk, start, end in chunk_text(text,
                                            cfg["chunk"]["tokens"],
                                            cfg["chunk"]["overlap"]):
            embedding = embed_texts([chunk])[0]
            upsert(
                [f"{file_path}-{start}-{end}"],
                [embedding],
                [{"path": str(file_path), "start": start, "end": end}],
                [chunk]
            )
    print("[green]Index complete[/green]")

@app.command()
def ask(q: str):
    cfg = load_config()
    load_model(cfg["embeddings"]["model"])
    hits = search(q)
    # Build context from top hits
    context = "\n\n".join(h['doc'] for h in hits)
    # Compose prompt for LLM
    prompt = f"Context:\n{context}\n\nQuestion: {q}\nAnswer:"
    # Call LLM
    answer = run_llm(prompt)
    print("[bold green]Answer:[/bold green]", answer)
    # Optionally, print citations as before
    for i, h in enumerate(hits, 1):
        print(f"[cyan]{i}[/cyan] {h['score']:.2f} {h['meta']['path']}")
        print(f"    {h['doc'][:200]}...\n")

if __name__ == "__main__":
    app()
