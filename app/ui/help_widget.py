import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from app.ui.chat_widget import ChatWidget


class HelpWidget(QWidget):
    def __init__(self, image: np.ndarray, chat_data: list) -> None:
        """
        A widget that displays an image and a ChatWidget in a visually appealing layout.

        Args:
            image (np.ndarray): The image to display (in RGB format).
            chat_data (list): Optional list of previous chat messages.
        """
        super().__init__()
        self.setWindowTitle("Help Assistant")
        self.setMinimumSize(800, 600)

        # Set background color and styling
        self.setStyleSheet(
            """
            QWidget {
                background-color: #2E3440;  /* Nordic dark background */
                color: #D8DEE9;  /* Nordic light gray */
            }
            QLabel {
                background-color: #3B4252;  /* Nordic gray */
                border: 1px solid #4C566A;  /* Nordic border gray */
                border-radius: 5px;
                color: #D8DEE9;  /* Nordic light gray */
            }
        """
        )

        # Convert the image to QPixmap
        image_qimage: QImage = QImage(
            image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888
        )
        image_pixmap: QPixmap = QPixmap.fromImage(image_qimage)
        image_pixmap = image_pixmap.scaled(
            400,
            300,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Image label
        self.image_label: QLabel = QLabel()
        self.image_label.setPixmap(image_pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        # Chat widget
        self.chat_widget: ChatWidget = ChatWidget(chat_data)

        # Layout for the image and chat widget
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.chat_widget)

        self.setLayout(main_layout)
