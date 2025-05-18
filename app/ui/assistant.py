import os
from langchain_cohere import ChatCohere

def ask_question_stream(question: str):
    api_key = os.environ.get("COHERE_API_KEY")
    llm = ChatCohere(
        api_key=api_key,
        model="command-r-plus"
    )
    for chunk in llm.stream(question):
        print(chunk.content, end='', flush=True)

question = input("Please ask a question: ")
ask_question_stream(question)