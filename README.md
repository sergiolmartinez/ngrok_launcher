# Ngrok Launcher

A Python-based GUI application to easily manage Ngrok tunnels with support for starting, stopping, and displaying tunnel details such as the public URL, request counts, and status. The public URL is clickable and opens in the browser.

## Features

- Start Ngrok tunnels for both default and custom domains.
- Display the public Ngrok URL, request counts, and tunnel status.
- Clickable public URL to open in the browser.
- Stop Ngrok processes and display logs.
- Error handling for Ngrok installation and API connection issues.
- Unit tests for core functionality using `unittest`.

## Requirements

- Python 3.8+.
- Ngrok installed and available in your system's PATH.
- Virtual environment (recommended).

### Python Packages

The project depends on several Python packages, listed in `requirements.txt`.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

The main dependencies are:

- `psutil`: Used to manage Ngrok processes.
- `requests`: Used to interact with the Ngrok API.
- `tkinter`: Used for the GUI.
- `unittest`: Built-in Python module for testing.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ngrok-launcher.git
   cd ngrok-launcher
   ```

2. Set up a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## Running Tests

The project includes unit tests for core functionality. You can run the tests with the following command:

```bash
python -m unittest discover
```

## Packaging as an Executable

To package this app as a standalone executable using **PyInstaller**, follow these steps:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller to create an executable:

   ```bash
   pyinstaller --onefile --windowed main.py
   ```

This will generate a `dist/` directory with the standalone executable.

## .gitignore

The project includes a `.gitignore` file to exclude unnecessary files like:

- Python bytecode (`*.pyc`, `__pycache__/`).
- Virtual environment (`.venv/`).
- Log files.
- Build artifacts from PyInstaller (`dist/`, `build/`).
- OS-specific files like `.DS_Store` (macOS) and `Thumbs.db` (Windows).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
