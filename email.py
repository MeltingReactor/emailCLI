#!/usr/bin/env python3

import os
# Force the exact display sockets explicitly inside Python
os.environ["WAYLAND_DISPLAY"] = "wayland-0"
os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"
import sys
import re
import argparse
import pyperclipfix as pyperclip

# 1. Force explicitly setting the Wayland clipboard engine
try:
    pyperclip.set_clipboard_backend("wl-clipboard")
except AttributeError:
    pass

# 2. Dynamically find the user's home directory path safely
HOME_DIR = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME_DIR, "Documents/emailCLI/config.scs")

try:
    with open(CONFIG_PATH, "r") as f:
        file_content = f.read()
except FileNotFoundError:
    print(f"Error: Configuration file not found at {CONFIG_PATH}", file=sys.stderr)
    sys.exit(1)

# 3. Setup argument parser for -n and -o flags
parser = argparse.ArgumentParser(description="SCS Email Clipboard Copy Tool")
group = parser.add_mutually_exclusive_group()
group.add_argument("-n", "--new", action="store_true")
group.add_argument("-o", "--old", action="store_true")
args = parser.parse_args()

# 4. Determine the mode
if args.new:
    mode = 1
elif args.old:
    mode = 0
else:
    default_match = re.search(r'default_mode=(\d+)', file_content)
    mode = int(default_match.group(1)) if default_match else 1

# 5. Extract the correct email address string
if mode == 1:
    match = re.search(r'\bemail="([^"]+)"', file_content)
else:
    match = re.search(r'old_email="([^"]+)"', file_content)

# 6. Copy directly to the Wayland clipboard and exit smoothly
if match:
    target_email = match.group(1)
    pyperclip.copy(target_email)
    sys.exit(0)
else:
    sys.exit(1)
