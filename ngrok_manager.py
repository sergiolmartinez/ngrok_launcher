import subprocess
import shutil
import requests  # To query the Ngrok API
import psutil
import time
from logger import logger

ngrok_process = None


def is_ngrok_installed():
    """Check if Ngrok is installed by trying to find it in the PATH."""
    return shutil.which("ngrok") is not None


def start_ngrok(port, domain=None):
    """Start Ngrok for the specified port and domain."""
    global ngrok_process
    if not is_ngrok_installed():
        logger.error("Ngrok is not installed or not found in PATH.")
        raise FileNotFoundError("Ngrok is not installed or not found in PATH.")

    stop_ngrok()  # Ensure any previous ngrok instance is stopped

    # Correctly format the command string
    if not domain:
        # Default Ngrok tunnel without custom domain
        command = ["ngrok", "http", str(port)]
    else:
        # Use the --domain flag for static/custom domains
        command = ["ngrok", "http", f"--domain={domain}", str(port)]

    try:
        logger.info(f"Starting Ngrok with command: {command}")
        # Start ngrok as a subprocess and capture the process object
        ngrok_process = subprocess.Popen(command)
        logger.info(f"Ngrok started with PID {ngrok_process.pid}")
    except Exception as e:
        logger.error(f"Failed to start Ngrok: {str(e)}")
        raise RuntimeError(f"Failed to start Ngrok: {str(e)}")


def stop_ngrok():
    """Stop the Ngrok process by killing the process tree."""
    global ngrok_process
    if ngrok_process is not None:
        try:
            logger.info("Attempting to stop Ngrok process by PID.")
            # Terminate the process using the process object if it's still running
            if ngrok_process.poll() is None:  # Check if process is still running
                ngrok_process.terminate()
                ngrok_process.wait(timeout=5)  # Wait for process to terminate
                logger.info(
                    f"Ngrok process with PID {ngrok_process.pid} terminated.")
            ngrok_process = None
        except Exception as e:
            logger.error(f"Failed to stop Ngrok: {str(e)}")
            raise RuntimeError(f"Failed to stop Ngrok: {str(e)}")
    else:
        logger.info("Ngrok process is not running.")


def get_ngrok_url():
    """Fetch the public URL of the active Ngrok tunnel by querying the Ngrok API."""
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        if response.status_code == 200:
            tunnels = response.json().get('tunnels')
            if tunnels:
                public_url = tunnels[0].get('public_url')
                logger.info(f"Ngrok public URL: {public_url}")
                return public_url
            else:
                logger.warning("No active tunnels found.")
                return None
        else:
            logger.error(f"Failed to query Ngrok API: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to the Ngrok API. Is Ngrok running?")
        raise RuntimeError(
            "Failed to retrieve Ngrok URL. Ngrok might not be running.")


def get_ngrok_url_with_retries(retries=5, delay=1):
    """Try to get the Ngrok URL with a few retries."""
    for _ in range(retries):
        url = get_ngrok_url()
        if url:
            return url
        logger.warning(f"Retrying to fetch Ngrok URL in {delay} seconds...")
        time.sleep(delay)
    return None


def get_ngrok_info():
    """Fetch detailed information about the active Ngrok tunnel."""
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        if response.status_code == 200:
            tunnels = response.json().get('tunnels')
            if tunnels:
                public_url = tunnels[0].get('public_url')
                metrics = tunnels[0].get('metrics', {})
                requests_count = metrics.get('http', {}).get('count', 0)
                status = tunnels[0].get('status', 'Unknown')

                tunnel_info = {
                    'public_url': public_url,
                    'requests_count': requests_count,
                    'status': status
                }
                logger.info(f"Ngrok tunnel info: {tunnel_info}")
                return tunnel_info
            else:
                logger.warning("No active tunnels found.")
                return None
        else:
            logger.error(f"Failed to query Ngrok API: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to the Ngrok API. Is Ngrok running?")
        raise RuntimeError(
            "Failed to retrieve Ngrok information. Ngrok might not be running.")
