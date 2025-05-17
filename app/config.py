import os

# Directory to save captured images
# Default is "captures" in the current working directory
SAVE_DIR = os.getenv("CAPTURE_SAVE_DIR", "captures")

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)
