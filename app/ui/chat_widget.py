import json
import threading

import requests
from langchain_ollama import OllamaLLM
from PyQt6.QtCore import Qt, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

class ChatCommunicator(QObject):
    token = pyqtSignal(str)
    enabled = pyqtSignal(bool)


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
                background-color: rgb(28, 32, 40);  /* Nordic dark background */
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
        self.input_field.returnPressed.connect(
            self.handle_send_message
        )  # Handle "Enter" key

        # Send button
        self.send_button: QPushButton = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send_message)
        self.communicator: ChatCommunicator = ChatCommunicator()
        self.communicator.token.connect(self.update_chat)
        self.communicator.enabled.connect(self.set_input_enabled)

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

        # State to track whether a response is being generated
        self.is_generating_response = False

    def handle_send_message(self) -> None:
        """
        Handles sending a message and streaming a response.
        """
        if self.is_generating_response:
            return  # Do nothing if a response is already being generated

        user_message = self.input_field.text().strip()  # Strip whitespace
        if not user_message:
            return  # Do nothing if the message is empty or only contains whitespace

        # Add user message to chat history
        self.chat_data.append(("User", user_message))
        self.chat_history.append(f"User: {user_message}\n\n")

        # Clear the input field
        self.input_field.clear()

        # Disable input while generating a response
        self.set_input_enabled(False)

        # Start a background thread to stream the response
        threading.Thread(
            target=self.stream_response_in_background, args=(user_message,)
        ).start()

    @pyqtSlot(str)
    def update_chat(self, token: str) -> None:
            """
            Updates the chat history with a streamed token.

            Args:
                token (str): The token to append to the chat history.
            """
            cursor = self.chat_history.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor.insertText(token)
            self.chat_history.setTextCursor(cursor)
            self.chat_history.ensureCursorVisible()

    def stream_response_in_background(self, user_message: str) -> None:
        """
        Streams the response in the background and updates the chat history.

        Args:
            data (dict): The data to send in the POST request.
        """
        # Add a placeholder for the assistant's response

        response_text = ""
        self.communicator.token.emit("Assistant: ")

        try:
            llm = OllamaLLM(model="llama3")
            for chunk in llm.stream(user_message):
                self.communicator.token.emit(chunk)  # Update the chat history with the token
                response_text += chunk

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Re-enable input after the response is complete
            self.chat_data.append(("Assistant", response_text))
            # self.set_input_enabled(True)
            self.communicator.enabled.emit(True)

    @pyqtSlot(bool)
    def set_input_enabled(self, enabled: bool) -> None:
        """
        Enables or disables the input field and send button.

        Args:
            enabled (bool): Whether to enable or disable the input.
        """
        self.input_field.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        self.is_generating_response = not enabled
