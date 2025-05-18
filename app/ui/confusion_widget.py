import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QImage, QPixmap
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.ui.help_widget import HelpWidget


class ConfusionWidget(QWidget):
    def __init__(
        self, image: np.ndarray, elapsed_time: str, confusion_score: float
    ) -> None:
        """
        A widget that displays an image, elapsed time, and a confusion score as a progress bar.

        Args:
            image (np.ndarray): The image to display (in RGB format).
            elapsed_time (str): The elapsed time as a formatted string (e.g., "00:01:23").
            confusion_score (float): The confusion score as a percentage (0 to 100).
        """
        super().__init__()

        # Store the image and initialize chat history
        self.image = image
        # self.image = np.transpose(image,(1,0,2)).copy()
        self.chat_history = (
            []
        )  # List to store chat messages (e.g., [("User", "Message")])

        # Set fixed size for the widget
        self.setFixedSize(220, 300)

        # Set background color, border, and rounded corners for the entire widget
        self.setStyleSheet(
            """
            QWidget {
                background-color: #3B4252;  /* Nordic dark gray */
                border: 1px solid #4C566A;  /* Nordic border gray */
                border-radius: 10px;
            }
        """
        )

        # Convert the image to QPixmap
        image_qimage: QImage = QImage(
            image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
        )

        image_pixmap: QPixmap = QPixmap.fromImage(image_qimage)
        image_pixmap = image_pixmap.scaled(
            200,
            150,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Image label
        self.image_label: QLabel = QLabel()
        self.image_label.setPixmap(image_pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Confusion score progress bar
        self.confusion_bar: QProgressBar = QProgressBar()
        self.confusion_bar.setValue(int(confusion_score))
        self.confusion_bar.setTextVisible(False)
        self.confusion_bar.setStyleSheet(
            f"""
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: #4C566A;  /* Nordic gray */
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0 y1:0, x2:{100 / confusion_score} y2:0, stop:0 #72CCA3, stop:0.5 #C7B767, stop:1 #F07878);  /* Nordic red */
                border-radius: 5px;
            }}
        """
        )

        # Elapsed time label
        self.elapsed_time_label: QLabel = QLabel(f"{elapsed_time}")
        self.elapsed_time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.elapsed_time_label.setStyleSheet("color: #D8DEE9;")  # Nordic light gray

        # Fullscreen button
        self.fullscreen_button: QPushButton = QPushButton("⛶")  # Fullscreen icon
        self.fullscreen_button.setFixedSize(30, 30)
        self.fullscreen_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                background-color: #4C566A;  /* Nordic gray */
                border: none;
                border-radius: 5px;
                color: #D8DEE9;  /* Nordic light gray */
            }
            QPushButton:hover {
                background-color: #5E81AC;  /* Nordic blue */
            }
        """
        )
        self.fullscreen_button.clicked.connect(self.open_help_widget)

        # Layout for timestamp and fullscreen button
        bottom_layout: QHBoxLayout = QHBoxLayout()
        bottom_layout.addWidget(self.elapsed_time_label)
        bottom_layout.addWidget(self.fullscreen_button)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.confusion_bar)
        main_layout.addLayout(bottom_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add padding inside the widget

        self.setLayout(main_layout)

    def open_help_widget(self) -> None:
        """
        Opens a HelpWidget with the stored image and chat history.
        """
        self.help_widget = HelpWidget(self.image, self.chat_history)
        self.help_widget.show()
