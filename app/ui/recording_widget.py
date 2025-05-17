from datetime import datetime
from typing import Callable, List, Tuple

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from app.recorder.recorder import capture_and_save
from app.ui.circle_button import ConcentricCircleButton


class RecordingWidget(QWidget):
    def __init__(self, switch_to_visualization_callback: Callable) -> None:
        super().__init__()
        self.switch_to_visualization_callback: Callable = (
            switch_to_visualization_callback
        )

        # Initialize UI components
        self.button: ConcentricCircleButton = ConcentricCircleButton("Start Recording")
        self.recording = False

        # Layout
        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.button)
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
        self.button.clicked.connect(self.update_state)

    def update_state(self) -> None:
        """
        Starts the recording process by showing the stop button,
        hiding the start button, and starting the timer.
        """
        if not self.recording:
            self.record_start_time = datetime.now()
            # self.stop_button.show()
            self.recording_data = []  # Reset recording data
            self.timer.start(1000)  # Call record_frame every 1000 ms (1 second)
            self.recording = True
            self.button.setText("Stop Recording")
            self.button.updateColor("#f15767", "#841a28")
            self.button.update()
        else:
            self.timer.stop()
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
            self.update_state()
