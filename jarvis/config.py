# ...existing code...
import yaml
from pathlib import Path

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
