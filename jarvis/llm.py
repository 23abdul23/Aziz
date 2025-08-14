# ...existing code...
import subprocess, json

def run_llm(prompt, model="llama3.1"):
    cmd = ["ollama", "run", model]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = proc.communicate(prompt)
    return out
