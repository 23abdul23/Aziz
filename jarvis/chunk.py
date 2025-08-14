# ...existing code...
def chunk_text(text, target_tokens=900, overlap=120):
    words = text.split()
    step = max(1, target_tokens - overlap)
    for i in range(0, len(words), step):
        window = words[i:i+target_tokens]
        if not window:
            break
        yield " ".join(window), i, i + len(window)
