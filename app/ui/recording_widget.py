from datetime import datetime
from typing import List, Tuple

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from app.recorder.recorder import capture_and_save


class RecordingWidget(QWidget):
    def __init__(self, switch_to_visualization_callback: callable) -> None:
        super().__init__()
        self.switch_to_visualization_callback: callable = (
            switch_to_visualization_callback
        )

        # Initialize UI components
        self.start_button: QPushButton = QPushButton("Start Recording")
        self.stop_button: QPushButton = QPushButton("Stop Recording")
        self.stop_button.hide()  # Hide stop button initially

        # Layout
        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # Timer for recording
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.record_frame)

        # Recording state
        self.record_start_time: datetime | None = None
        self.recording_data: List[Tuple] = (
            []
        )  # List to store tuples from capture_and_save

        # Connect buttons
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

    def start_recording(self) -> None:
        """
        Starts the recording process by showing the stop button,
        hiding the start button, and starting the timer.
        """
        self.record_start_time = datetime.now()
        self.start_button.hide()
        self.stop_button.show()
        self.recording_data = []  # Reset recording data
        self.timer.start(1000)  # Call record_frame every 1000 ms (1 second)

    def stop_recording(self) -> None:
        """
        Stops the recording process by hiding the stop button,
        showing the start button, and stopping the timer.
        """
        self.timer.stop()
        self.stop_button.hide()
        self.start_button.show()

        # Switch to visualization view
        self.switch_to_visualization_callback(
            self.recording_data, self.record_start_time
        )

    def record_frame(self) -> None:
        """
        Captures a frame using capture_and_save and appends the result
        to the recording data list.
        """
        try:
            result: Tuple = capture_and_save()
            self.recording_data.append(result)
        except Exception as e:
            print(f"Error during recording: {e}")
            self.stop_recording()
