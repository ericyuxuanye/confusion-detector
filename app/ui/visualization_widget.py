from datetime import datetime, timedelta
from typing import List, Tuple

from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.processing.aggregate import process_recording_data
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

        # Process the recording data into segments
        self.processed_segments = process_recording_data(recording_data)
        self.record_start_time = record_start_time

        # Dropdown menu for sorting options
        self.sort_dropdown: QComboBox = QComboBox()
        self.sort_dropdown.addItem("Sort by Confusion Score (Descending)")
        self.sort_dropdown.addItem("Sort by Timestamp")
        self.sort_dropdown.currentIndexChanged.connect(self.update_sorting)

        # Default sorting: by confusion score (descending)
        self.sort_widgets_by_confusion_score()

        # Add confusion widgets to the grid layout
        self.populate_grid()

        # Set up the scroll area
        content_widget.setLayout(self.layout)
        scroll_area.setWidget(content_widget)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        dropdown_layout: QHBoxLayout = QHBoxLayout()
        dropdown_layout.addWidget(self.sort_dropdown)
        dropdown_layout.setContentsMargins(0, 0, 0, 10)  # Add spacing below dropdown

        main_layout.addLayout(dropdown_layout)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def populate_grid(self) -> None:
        """
        Populates the grid layout with ConfusionWidgets based on the current sorting.
        """
        # Clear the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                self.layout.removeWidget(widget)
                widget.setParent(None)

        # Add widgets to the grid layout
        for i, (
            screenshot,
            avg_confusion_score,
            first_timestamp,
            last_timestamp,
        ) in enumerate(self.processed_segments):
            # Calculate elapsed time strings
            elapsed_to_first: timedelta = first_timestamp - self.record_start_time
            elapsed_to_last: timedelta = last_timestamp - self.record_start_time
            elapsed_str: str = (
                f"{str(elapsed_to_first).split('.')[0]}-{str(elapsed_to_last).split('.')[0]}"
            )

            # Create a ConfusionWidget
            confusion_widget: ConfusionWidget = ConfusionWidget(
                screenshot, elapsed_str, avg_confusion_score
            )

            # Add the widget to the grid layout
            self.layout.addWidget(confusion_widget)  # 3 widgets per row
        self._set_curr_layout()

    def sort_widgets_by_confusion_score(self) -> None:
        """
        Sorts the processed segments by average confusion score in descending order.
        """
        self.processed_segments.sort(key=lambda x: x[1], reverse=True)

    def sort_widgets_by_timestamp(self) -> None:
        """
        Sorts the processed segments by timestamp (in the same order as the input list).
        """
        self.processed_segments.sort(key=lambda x: x[2])  # Sort by first_timestamp

    def update_sorting(self) -> None:
        """
        Updates the sorting of the ConfusionWidgets based on the selected dropdown option.
        """
        if self.sort_dropdown.currentIndex() == 0:
            self.sort_widgets_by_confusion_score()
        elif self.sort_dropdown.currentIndex() == 1:
            self.sort_widgets_by_timestamp()

        # Repopulate the grid with the new sorting
        self.populate_grid()

    def resizeEvent(self, event) -> None:
        """
        Dynamically adjust the number of widgets per row based on the window size.
        """
        super().resizeEvent(event)
        if self.layout.count() == 0:
            return

        self._set_curr_layout()

    def _set_curr_layout(self) -> None:
        """
        Rearranges widgets in the grid layout based on the current window width.
        """
        widget_width: int = (
            220  # Approximate width of each ConfusionWidget (200px + padding)
        )
        num_columns: int = max(1, self.width() // widget_width)

        # Collect all widgets
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
