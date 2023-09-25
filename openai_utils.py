from dotenv import load_dotenv
import os
import openai

import time

from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = "gpt-4-0613"
CUSTOM_INSTRUCTIONS = "You are a helpful assistant."
STREAM = False

def set_custom_instruction(instructions):
    global CUSTOM_INSTRUCTIONS
    CUSTOM_INSTRUCTIONS = instructions

def set_stream(choice):
    global STREAM
    STREAM = choice

def list_openai_models():
    models = openai.Model.list()
    return models

def create_chat_response(user_messages="", chat_history=None):
    console = Console()

    log_messages = []

    if chat_history:
        log_messages.extend(chat_history)
    else:
        log_messages.append({'role': 'system', 'content': CUSTOM_INSTRUCTIONS})

    if user_messages:
        # Split user messages by newline and add them to the log_messages
        user_messages_list = user_messages.split('\n')
        for user_message_content in user_messages_list:
            if user_message_content.strip() != "":
                user_message = {"role": "user", "content": user_message_content.strip()}
                log_messages.append(user_message)

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=log_messages,
        stream=STREAM
    )

    answer = ""

    if STREAM:
        for chunk in response:
            event_text = chunk['choices'][0]['delta']
            answer = answer + (event_text.get('content', ''))
            console.print(event_text.get('content', ''), end='', markup=True)
    else:
        for i in track(response.choices[0].message.content, description="Loading..."):
            answer = response.choices[0].message.content

    # Add assistant's reply to the log_messages
    assistant_message = {"role": "assistant", "content": answer}
    log_messages.append(assistant_message)

    return log_messages, answer