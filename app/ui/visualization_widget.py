from datetime import datetime, timedelta
from typing import List, Tuple

from PyQt6.QtWidgets import QGridLayout, QScrollArea, QVBoxLayout, QWidget

from app.ui.confusion_widget import ConfusionWidget


class VisualizationWidget(QWidget):
    def __init__(
        self, recording_data: List[Tuple], record_start_time: datetime
    ) -> None:
        super().__init__()

        # Scroll area to enable scrolling
        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Widget to hold the layout
        content_widget: QWidget = QWidget()
        self.layout: QGridLayout = QGridLayout()

        # Add confusion widgets to the grid layout
        for i, (screenshot, _, timestamp) in enumerate(recording_data):
            # Calculate elapsed time
            elapsed_time: timedelta = timestamp - record_start_time
            elapsed_str: str = str(
                timedelta(seconds=elapsed_time.total_seconds())
            ).split(".")[0]

            # Generate a dummy confusion score for now (replace with actual logic later)
            # confusion_score: float = np.random.uniform(0, 100)
            confusion_score: float = 69

            # Create a ConfusionWidget
            confusion_widget: ConfusionWidget = ConfusionWidget(
                screenshot, elapsed_str, confusion_score
            )

            # Add the widget to the grid layout
            self.layout.addWidget(
                confusion_widget, i // 3, i % 3
            )  # 3 widgets per row (default)

        content_widget.setLayout(self.layout)
        scroll_area.setWidget(content_widget)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def resizeEvent(self, event) -> None:
        """
        Dynamically adjust the number of widgets per row based on the window size.
        """
        super().resizeEvent(event)
        if self.layout.count() == 0:
            return

        # Calculate the number of widgets per row based on the current window width
        widget_width: int = (
            220  # Approximate width of each ConfusionWidget (200px + padding)
        )
        num_columns: int = max(1, self.width() // widget_width)

        # Rearrange widgets in the grid layout
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            self.layout.addWidget(widget, i // num_columns, i % num_columns)
