import os
from datetime import datetime

import cv2
import numpy as np
import pyautogui

from app.config import SAVE_DIR


def capture_screenshot() -> np.ndarray:
    """
    Captures a screenshot of the current screen.

    Returns:
        np.ndarray: The screenshot as a NumPy array in RGB format.
    """
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)


def capture_webcam_frame() -> np.ndarray:
    """
    Captures a single frame from the default webcam.

    Returns:
        np.ndarray: The webcam frame as a NumPy array in BGR format.
    """
    cap = cv2.VideoCapture(0)  # Open the default webcam
    ret, frame = cap.read()
    cap.release()  # Release the webcam
    if not ret:
        raise RuntimeError("Failed to capture webcam frame.")
    return frame


def save_image(image: np.ndarray, prefix: str, timestamp: datetime) -> str:
    """
    Saves an image to the SAVE_DIR with a timestamped filename.

    Args:
        image (np.ndarray): The image to save.
        prefix (str): The prefix for the filename (e.g., 'screenshot' or 'webcam').
        timestamp (datetime): The timestamp to include in the filename.

    Returns:
        str: The file path of the saved image.
    """
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp_str}.png"
    filepath = os.path.join(SAVE_DIR, filename)
    if prefix == "screenshot":
        # Convert screenshot from RGB to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filepath, image)
    return filepath


def get_image_filepath(prefix: str, timestamp: datetime) -> str:
    """
    Returns the file path of an image (screenshot or webcam frame) saved with the given timestamp.

    Args:
        prefix (str): The prefix for the filename (e.g., 'screenshot' or 'webcam').
        timestamp (datetime): The timestamp of the image.

    Returns:
        str: The file path of the image.
    """
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp_str}.png"
    return os.path.join(SAVE_DIR, filename)


def capture_and_save() -> tuple[np.ndarray, np.ndarray]:
    """
    Captures a screenshot and a webcam frame, saves them with timestamps,
    and returns their NumPy representations.

    Returns:
        tuple[np.ndarray, np.ndarray, datetime]: A tuple containing:
            - np.ndarray: The screenshot as a NumPy array in RGB format.
            - np.ndarray: The webcam frame as a NumPy array in BGR format.
            - datetime: The timestamp of the capture.
    """
    timestamp = datetime.now()

    # Capture screenshot
    screenshot = capture_screenshot()

    # Capture webcam frame
    webcam_frame = capture_webcam_frame()

    return screenshot, webcam_frame, timestamp
