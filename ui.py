import tkinter as tk
from tkinter import messagebox
import webbrowser  # To open URLs in the default web browser
from ngrok_manager import start_ngrok, stop_ngrok, get_ngrok_url_with_retries
from config_manager import load_last_config, save_config
from logger import logger


class NgrokLauncher:
    """Class representing the Ngrok Launcher UI."""

    def __init__(self, root):
        self.root = root
        self.ngrok_info = None  # Store Ngrok tunnel information
        self.setup_ui()
        self.load_previous_config()

    def setup_ui(self):
        """Initialize the Ngrok Launcher UI components."""
        self.root.title(f"Ngrok Launcher - v1.0.0")

        # Port input
        self.label_port = tk.Label(self.root, text="Port:")
        self.label_port.grid(row=0, column=0, padx=10, pady=10)
        self.entry_port = tk.Entry(self.root)
        self.entry_port.grid(row=0, column=1, padx=10, pady=10)

        # Domain input
        self.label_domain = tk.Label(
            self.root, text="Custom Domain (optional):")
        self.label_domain.grid(row=1, column=0, padx=10, pady=10)
        self.entry_domain = tk.Entry(self.root)
        self.entry_domain.grid(row=1, column=1, padx=10, pady=10)

        # Status indicator
        self.status_label = tk.Label(
            self.root, text="Ngrok status: Stopped", fg="red")
        self.status_label.grid(row=2, column=0, columnspan=2)

        # URL display (clickable)
        self.url_label = tk.Label(
            self.root, text="Ngrok URL: Not available", fg="blue", cursor="hand2")
        self.url_label.grid(row=3, column=0, columnspan=2)
        # Bind click event to open the URL
        self.url_label.bind("<Button-1>", self.open_url)

        # Additional Tunnel Information (requests count, status)
        self.info_label = tk.Label(
            self.root, text="Requests: 0 | Status: Unknown", fg="green")
        self.info_label.grid(row=4, column=0, columnspan=2)

        # Start/Stop buttons
        self.button_start_default = tk.Button(
            self.root, text="Start Ngrok (Default URL)", command=self.start_ngrok_default)
        self.button_start_default.grid(row=5, column=0, padx=10, pady=10)

        self.button_start_custom = tk.Button(
            self.root, text="Start Ngrok (Custom Domain)", command=self.start_ngrok_custom)
        self.button_start_custom.grid(row=5, column=1, padx=10, pady=10)

        self.button_stop = tk.Button(
            self.root, text="Stop Ngrok", command=self.stop_ngrok)
        self.button_stop.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def load_previous_config(self):
        """Load the previous configuration into the UI fields."""
        config = load_last_config()
        self.entry_port.insert(0, config["port"])
        self.entry_domain.insert(0, config["domain"])

    def update_status(self, status, color="red"):
        """Update the status label."""
        self.status_label.config(text=f"Ngrok status: {status}", fg=color)

    def update_url(self, url=None):
        """Update the displayed Ngrok public URL."""
        self.ngrok_info = url
        if url:
            self.url_label.config(
                text=f"Ngrok URL: {url}", fg="green", cursor="hand2")
        else:
            self.url_label.config(
                text="Ngrok URL: Not available", fg="red", cursor="")

    def open_url(self, event):
        """Open the Ngrok URL in the default web browser when clicked."""
        if self.ngrok_info:
            webbrowser.open(self.ngrok_info)

    def start_ngrok_default(self):
        """Start Ngrok using default URL."""
        port = self.entry_port.get()
        if not port.isdigit():
            messagebox.showerror("Error", "Please enter a valid port number")
            return
        try:
            start_ngrok(port)
            save_config(port, self.entry_domain.get())
            self.update_status("Running", "green")

            # Fetch the public URL from Ngrok with retries
            url = get_ngrok_url_with_retries()
            if url:
                self.update_url(url)
            else:
                self.update_url(None)

        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
            logger.error(str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(str(e))

    def start_ngrok_custom(self):
        """Start Ngrok with a custom domain."""
        port = self.entry_port.get()
        domain = self.entry_domain.get()
        if not port.isdigit():
            messagebox.showerror("Error", "Please enter a valid port number")
            return
        if not domain:
            messagebox.showerror("Error", "Please enter a custom domain")
            return
        try:
            start_ngrok(port, domain)
            save_config(port, domain)
            self.update_status("Running", "green")

            # Fetch the public URL from Ngrok with retries
            url = get_ngrok_url_with_retries()
            if url:
                self.update_url(url)
            else:
                self.update_url(None)

        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
            logger.error(str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(str(e))

    def stop_ngrok(self):
        """Stop the running Ngrok process."""
        try:
            stop_ngrok()
            self.update_status("Stopped", "red")
            self.update_url(None)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop Ngrok: {str(e)}")
            logger.error(f"Failed to stop Ngrok: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NgrokLauncher(root)
    root.mainloop()
