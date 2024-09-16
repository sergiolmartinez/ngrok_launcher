import logging
import os

# Set up logging configuration
log_dir = os.path.join(os.path.expanduser("~"), "ngrok_gui_logs")
os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists
log_file = os.path.join(log_dir, "ngrok_gui.log")


def setup_logger():
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()


logger = setup_logger()
