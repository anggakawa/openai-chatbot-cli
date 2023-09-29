from dotenv import load_dotenv
import os
import openai

import time

from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track

from prompt_toolkit import print_formatted_text as print, HTML
from prompt_toolkit.styles import Style

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

def stream_response(user_messages="", chat_history=None):
    log_messages = []

    if chat_history:
        log_messages.extend(chat_history)
    else:
        log_messages.append({'role': 'system', 'content': CUSTOM_INSTRUCTIONS})

    if user_messages:
        user_message = {"role": "user", "content": user_messages.strip()}
        log_messages.append(user_message)

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=log_messages,
        stream=STREAM
    )

    return log_messages, response

def create_chat_response(user_messages="", chat_history=None):
    console = Console()

    log_messages = []

    if chat_history:
        log_messages.extend(chat_history)
    else:
        log_messages.append({'role': 'system', 'content': CUSTOM_INSTRUCTIONS})

    if user_messages:
        user_message = {"role": "user", "content": user_messages.strip()}
        log_messages.append(user_message)

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=log_messages,
        stream=STREAM
    )

    answer = ""

    if STREAM:
        prompt_style = Style.from_dict({
            'prompt': 'ansigreen bold',
            'input': '',
        })
        for chunk in response:
            event_text = chunk['choices'][0]['delta']
            answer = answer + (event_text.get('content', ''))
            if event_text.get('content'):
                print(HTML(f"<ansigreen>{event_text.get('content', '')}</ansigreen>"), end='', style=prompt_style)
            else:
                print('')
            # console.print(event_text.get('content', ''), end='', markup=True, style="green1")
    else:
        for i in track(response.choices[0].message.content, description="Loading..."):
            answer = response.choices[0].message.content

    # Add assistant's reply to the log_messages
    assistant_message = {"role": "assistant", "content": answer}
    log_messages.append(assistant_message)

    return log_messages, answer