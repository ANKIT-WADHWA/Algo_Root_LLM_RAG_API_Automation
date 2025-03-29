import os
import webbrowser
import psutil
import subprocess

# ✅ Application Control
def open_chrome():
    webbrowser.open("https://www.google.com")

def open_calculator():
    os.system("calc")

def open_notepad():
    os.system("notepad")

# ✅ System Monitoring
def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    ram = psutil.virtual_memory()
    return f"RAM Usage: {ram.percent}%"


def list_files(directory="."):
    """Lists files in the specified directory."""
    try:
        files = os.listdir(directory)
        return f"Files in '{directory}': {', '.join(files)}"
    except Exception as e:
        return f"Error listing files: {e}"