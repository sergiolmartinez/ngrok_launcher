import subprocess
import shutil
import requests  # To query the Ngrok API
import psutil
from logger import logger

# Store the Ngrok process globally
ngrok_process = None


def is_ngrok_installed():
    """Check if Ngrok is installed by trying to find it in the system PATH."""
    return shutil.which("ngrok") is not None


def start_ngrok(port, domain=None):
    """Start Ngrok for the specified port and domain, or default URL."""
    global ngrok_process
    if not is_ngrok_installed():
        logger.error("Ngrok is not installed or not found in PATH.")
        raise FileNotFoundError("Ngrok is not installed or not found in PATH.")

    # Stop any previously running Ngrok instances
    stop_ngrok()

    # Build the correct Ngrok command
    if not domain:
        # Default Ngrok tunnel (dynamic URL)
        command = f"ngrok http {port}"
    else:
        # Static/custom domain for Ngrok tunnel
        command = f"ngrok http --domain={domain} {port}"

    try:
        logger.info(f"Starting Ngrok with command: {command}")
        # Start Ngrok as a subprocess and capture the process object
        ngrok_process = subprocess.Popen(command, shell=True)
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
            # Kill the Ngrok process using psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if 'ngrok' in proc.info['name'].lower():
                    logger.info(
                        f"Found Ngrok process with PID {proc.info['pid']}, terminating it.")
                    parent = psutil.Process(proc.info['pid'])
                    for child in parent.children(recursive=True):
                        child.terminate()  # Terminate child processes
                    parent.terminate()  # Terminate the parent process
                    parent.wait(timeout=5)  # Wait for the process to terminate
                    logger.info(
                        f"Successfully terminated Ngrok process with PID {proc.info['pid']}.")
                    break
            ngrok_process = None
        except psutil.NoSuchProcess:
            logger.error("Ngrok process not found.")
        except Exception as e:
            logger.error(f"Failed to stop Ngrok: {str(e)}")
            raise RuntimeError(f"Failed to stop Ngrok: {str(e)}")


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
