import json
import os

CONFIG_FILE = os.path.expanduser("~/.ngrok_gui_config.json")


def load_last_config():
    """Load the last configuration from a JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"port": "", "domain": ""}


def save_config(port, domain):
    """Save the user's port and domain configuration to a JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"port": port, "domain": domain}, f)
