import sys
from datetime import datetime
from typing import List, Tuple

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from app.ui.recording_widget import RecordingWidget
from app.ui.visualization_widget import VisualizationWidget
from torch.multiprocessing import Pool, set_start_method


class WorkerCommunicator(QObject):
    data_ready = pyqtSignal(int, float)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Recorder App")

        # Stacked widget to manage views
        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        set_start_method('fork', force=True)
        self.pool = Pool(8)
        # how many frames we finished
        self.num_frames = 0
        self.results = []
        self.finished_recording = False

        self.communicator = WorkerCommunicator()

        # Recording view
        self.recording_widget: RecordingWidget = RecordingWidget(
            self.finish_callback,
            self.pool,
            self.communicator,
        )
        self.stacked_widget.addWidget(self.recording_widget)
        self.communicator.data_ready.connect(self.ui_callback)

    def finish_callback(
        self, recording_data: List[Tuple], record_start_time: datetime
    ) -> None:
        """
        Switches to the visualization view after recording is stopped.
        """
        print(f"Finished recording, len(recording_data)={len(recording_data)}")
        self.finished_recording = True
        self.recording_data = recording_data
        self.record_start_time = record_start_time

    @pyqtSlot(int, float)
    def ui_callback(self, id: int, confusion: float):
        self.num_frames += 1
        print(f"Got callback id: {id}, num frames: {self.num_frames}")
        while len(self.results) <= id:
            self.results.append(None)

        self.results[id] = confusion

        if self.finished_recording and self.num_frames == len(self.recording_data):
            visualization_widget: VisualizationWidget = VisualizationWidget(
                self.recording_data, self.record_start_time, self.results,
            )
            self.stacked_widget.addWidget(visualization_widget)
            self.stacked_widget.setCurrentWidget(visualization_widget)
            self.resize(1000, 500)



if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
