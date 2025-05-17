import sys
from datetime import datetime, timedelta
from typing import List, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)

from app.recorder.recorder import capture_and_save


class RecordingWidget(QWidget):
    def __init__(self, switch_to_visualization_callback: callable) -> None:
        super().__init__()
        self.switch_to_visualization_callback: callable = switch_to_visualization_callback

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
        self.recording_data: List[Tuple] = []  # List to store tuples from capture_and_save

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
        self.switch_to_visualization_callback(self.recording_data, self.record_start_time)

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


class VisualizationWidget(QWidget):
    def __init__(self, recording_data: List[Tuple], record_start_time: datetime) -> None:
        super().__init__()

        # Scroll area to enable scrolling
        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Widget to hold the layout
        content_widget: QWidget = QWidget()
        layout: QGridLayout = QGridLayout()

        for i, (screenshot, webcam_frame, timestamp) in enumerate(recording_data):
            # Calculate elapsed time
            elapsed_time: timedelta = timestamp - record_start_time
            elapsed_str: str = str(timedelta(seconds=elapsed_time.total_seconds())).split(".")[0]

            # Convert screenshot to QPixmap and scale it
            screenshot_image: QImage = QImage(
                screenshot.data,
                screenshot.shape[1],
                screenshot.shape[0],
                QImage.Format.Format_RGB888,
            )
            screenshot_pixmap: QPixmap = QPixmap.fromImage(screenshot_image)
            screenshot_pixmap = screenshot_pixmap.scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )

            # Convert webcam frame to QPixmap and scale it
            webcam_image: QImage = QImage(
                webcam_frame.data,
                webcam_frame.shape[1],
                webcam_frame.shape[0],
                QImage.Format.Format_BGR888,
            )
            webcam_pixmap: QPixmap = QPixmap.fromImage(webcam_image)
            webcam_pixmap = webcam_pixmap.scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )

            # Add screenshot and webcam frame side-by-side
            screenshot_label: QLabel = QLabel()
            screenshot_label.setPixmap(screenshot_pixmap)
            layout.addWidget(screenshot_label, i, 0)

            webcam_label: QLabel = QLabel()
            webcam_label.setPixmap(webcam_pixmap)
            layout.addWidget(webcam_label, i, 1)

            # Add elapsed time label
            elapsed_label: QLabel = QLabel(f"Elapsed: {elapsed_str}")
            layout.addWidget(elapsed_label, i, 2)

        content_widget.setLayout(layout)
        scroll_area.setWidget(content_widget)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Recorder App")

        # Stacked widget to manage views
        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Recording view
        self.recording_widget: RecordingWidget = RecordingWidget(self.switch_to_visualization)
        self.stacked_widget.addWidget(self.recording_widget)

    def switch_to_visualization(self, recording_data: List[Tuple], record_start_time: datetime) -> None:
        """
        Switches to the visualization view after recording is stopped.
        """
        visualization_widget: VisualizationWidget = VisualizationWidget(recording_data, record_start_time)
        self.stacked_widget.addWidget(visualization_widget)
        self.stacked_widget.setCurrentWidget(visualization_widget)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
