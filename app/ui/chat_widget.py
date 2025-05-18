from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ChatWidget(QWidget):
    def __init__(self, chat_data: list) -> None:
        """
        A widget that displays a chatbot-like interface.

        Args:
            chat_data (list): Optional list of previous chat messages.
        """
        super().__init__()

        # Set background color and styling
        self.setStyleSheet(
            """
            QWidget {
                background-color: #2E3440;  /* Nordic dark background */
                color: #D8DEE9;  /* Nordic light gray */
            }
            QTextEdit, QLineEdit {
                background-color: #3B4252;  /* Nordic gray */
                border: 1px solid #4C566A;  /* Nordic border gray */
                border-radius: 5px;
                color: #D8DEE9;  /* Nordic light gray */
            }
            QPushButton {
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

        # Chat data
        self.chat_data = chat_data

        # Chat history display
        self.chat_history: QTextEdit = QTextEdit()
        self.chat_history.setReadOnly(True)

        # Populate chat history if chat_data exists
        for sender, message in self.chat_data:
            self.chat_history.append(f"{sender}: {message}")

        # Input field for user messages
        self.input_field: QLineEdit = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.handle_send_message)  # Handle "Enter" key

        # Send button
        self.send_button: QPushButton = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send_message)

        # Layout for input field and send button
        input_layout: QHBoxLayout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(QLabel("Chat Assistant"))  # Title label
        main_layout.addWidget(self.chat_history)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

    def handle_send_message(self) -> None:
        """
        Handles sending a message and displaying a mock response.
        """
        user_message = self.input_field.text().strip()  # Strip whitespace
        if not user_message:
            return  # Do nothing if the message is empty or only contains whitespace

        # Add user message to chat history
        self.chat_data.append(("User", user_message))
        self.chat_history.append(f"User: {user_message}")

        # Mock assistant response
        assistant_response = "This is a mock response from the assistant."
        self.chat_data.append(("Assistant", assistant_response))
        self.chat_history.append(f"Assistant: {assistant_response}")

        # Clear the input field
        self.input_field.clear()
