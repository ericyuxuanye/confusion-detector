import numpy as np
from typing import List, Tuple
from datetime import datetime
import random


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

    # Helper function to compute mean squared error between two images
    def mean_squared_error(img1: np.ndarray, img2: np.ndarray) -> float:
        return np.mean((img1.astype("float") - img2.astype("float")) ** 2)

    # Threshold for detecting slide changes (tune this value as needed)
    mse_threshold = 1000.0

    # Partition the data into segments based on slide changes
    segments = []
    current_segment = [recording_data[0]]

    for i in range(1, len(recording_data)):
        prev_screenshot, _, _ = recording_data[i - 1]
        curr_screenshot, _, _ = recording_data[i]

        # Compute MSE between consecutive screenshots
        mse = mean_squared_error(prev_screenshot, curr_screenshot)

        if mse > mse_threshold:
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
