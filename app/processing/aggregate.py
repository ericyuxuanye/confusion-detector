import random
from datetime import datetime
from typing import List, Tuple

import cv2
import numpy as np


def process_recording_data(
    recording_data: List[Tuple[np.ndarray, np.ndarray, datetime]],
) -> List[Tuple[np.ndarray, float, datetime, datetime]]:
    """
    Processes the recording data to partition it into segments based on slide changes
    and computes the average confusion score for each segment.

    Args:
        recording_data (List[Tuple[np.ndarray, np.ndarray, datetime]]): A list of tuples where each tuple contains:
            - A screenshot (np.ndarray)
            - A webcam frame (np.ndarray)
            - A timestamp (datetime)

    Returns:
        List[Tuple[np.ndarray, float, datetime, datetime]]: A list of tuples where each tuple contains:
            - The first screenshot from the segment (np.ndarray)
            - The average confusion score for the segment (float)
            - The timestamp of the first screenshot in the segment (datetime)
            - The timestamp of the last screenshot in the segment (datetime)
    """
    if not recording_data:
        return []

    # Partition the data into segments based on slide changes
    segments = []
    current_segment = [recording_data[0]]

    for i in range(1, len(recording_data)):
        prev_screenshot, _, _ = recording_data[i - 1]
        curr_screenshot, _, _ = recording_data[i]

        if not _are_frames_similar(prev_screenshot, curr_screenshot):
            # Slide change detected, start a new segment
            segments.append(current_segment)
            current_segment = [recording_data[i]]
        else:
            # Add to the current segment
            current_segment.append(recording_data[i])

    # Add the last segment
    if current_segment:
        segments.append(current_segment)

    # Compute the average confusion score for each segment
    result = []
    for segment in segments:
        first_screenshot, _, first_timestamp = segment[0]
        last_screenshot, _, last_timestamp = segment[-1]

        # Generate random confusion scores for each webcam frame in the segment
        confusion_scores = [random.uniform(0, 100) for _ in segment]

        # Compute the average confusion score for the segment
        avg_confusion_score = sum(confusion_scores) / len(confusion_scores)

        # Append the result for this segment
        result.append(
            (first_screenshot, avg_confusion_score, first_timestamp, last_timestamp)
        )

    return result


def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Applies Gaussian blurring to an image.

    Args:
        image (np.ndarray): The input image.
        kernel_size (int): The size of the Gaussian kernel. Must be odd.

    Returns:
        np.ndarray: The blurred image.
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def _are_frames_similar_gaussian_blur(
    frame1: np.ndarray,
    frame2: np.ndarray,
    threshold: float = 40.0**2,
) -> bool:
    """
    Check if two frames are similar based on a threshold after applying Gaussian blur.

    Args:
        frame1 (np.ndarray): The first frame.
        frame2 (np.ndarray): The second frame.
        threshold (float): The similarity threshold.

    Returns:
        bool: True if the frames are similar, False otherwise.
    """
    # Helper function to compute mean squared error between two images
    def mean_squared_error(img1: np.ndarray, img2: np.ndarray) -> float:
        return np.mean((img1.astype("float") - img2.astype("float")) ** 2)

    blurred_frame1 = apply_gaussian_blur(frame1)
    blurred_frame2 = apply_gaussian_blur(frame2)
    return mean_squared_error(blurred_frame1, blurred_frame2) < threshold

def _are_frames_similar(
    frame1: np.ndarray,
    frame2: np.ndarray,
) -> bool:
    """
    Check if two frames are similar based on a threshold.

    Args:
        frame1 (np.ndarray): The first frame.
        frame2 (np.ndarray): The second frame.

    Returns:
        bool: True if the frames are similar, False otherwise.
    """

    return _are_frames_similar_gaussian_blur(frame1, frame2)
