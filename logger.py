import logging

# Configure logger to log to file
logging.basicConfig(
    filename="ngrok_launcher.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

logger = logging.getLogger()
