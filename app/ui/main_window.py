import sys
from datetime import datetime
from typing import List, Tuple

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from app.ui.recording_widget import RecordingWidget
from app.ui.visualization_widget import VisualizationWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Recorder App")

        # Stacked widget to manage views
        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Recording view
        self.recording_widget: RecordingWidget = RecordingWidget(
            self.switch_to_visualization
        )
        self.stacked_widget.addWidget(self.recording_widget)

    def switch_to_visualization(
        self, recording_data: List[Tuple], record_start_time: datetime
    ) -> None:
        """
        Switches to the visualization view after recording is stopped.
        """
        visualization_widget: VisualizationWidget = VisualizationWidget(
            recording_data, record_start_time
        )
        self.stacked_widget.addWidget(visualization_widget)
        self.stacked_widget.setCurrentWidget(visualization_widget)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
