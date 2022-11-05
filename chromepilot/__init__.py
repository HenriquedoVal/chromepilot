import sys
import os


if sys.platform == 'linux':
    path = os.path.expanduser('~/.cache/chromepilot/bin/')

elif sys.platform == 'win32':
    path = os.environ['LOCALAPPDATA'] + '\\chromepilot\\bin\\'

os.makedirs(path, exist_ok=True)
INSTALL_PATH = os.path.abspath(path)
