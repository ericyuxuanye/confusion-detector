from datetime import datetime, timedelta
from typing import List, Tuple

from PyQt6.QtWidgets import QGridLayout, QScrollArea, QVBoxLayout, QWidget

from app.ui.confusion_widget import ConfusionWidget
from app.processing.aggregate import process_recording_data


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

        # Process the recording data into segments
        processed_segments = process_recording_data(recording_data)
        print(len(processed_segments), "segments")

        # Add confusion widgets to the grid layout
        for i, (
            screenshot,
            avg_confusion_score,
            first_timestamp,
            last_timestamp,
        ) in enumerate(processed_segments):
            # Calculate elapsed time strings
            elapsed_to_first: timedelta = first_timestamp - record_start_time
            elapsed_to_last: timedelta = last_timestamp - record_start_time
            elapsed_str: str = (
                f"{str(elapsed_to_first).split('.')[0]}-{str(elapsed_to_last).split('.')[0]}"
            )

            # Create a ConfusionWidget
            confusion_widget: ConfusionWidget = ConfusionWidget(
                screenshot, elapsed_str, avg_confusion_score
            )
            
            self.layout.addWidget(confusion_widget)


        self._set_curr_layout()
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
        
        self._set_curr_layout()

    def _set_curr_layout(self) -> None:
        # Calculate the number of widgets per row based on the current window width
        widget_width: int = (
            220  # Approximate width of each ConfusionWidget (200px + padding)
        )
        num_columns: int = max(1, self.width() // widget_width)
        # clear the layout
        widgets: List[QWidget] = []
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widgets.append(widget)
                self.layout.removeWidget(widget)
                widget.setParent(None)

        # Rearrange widgets in the grid layout
        for i, widget in enumerate(reversed(widgets)):
            self.layout.addWidget(widget, i // num_columns, i % num_columns)
