import argparse

import os
from openai_utils import create_chat_response, set_custom_instruction, set_stream, stream_response
import utils

from functools import partial

from prompt_toolkit import print_formatted_text as print, HTML
from prompt_toolkit import PromptSession
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, WindowAlign
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Box, Label, TextArea, SearchToolbar, Frame, Button
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.document import Document
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.clipboard import Clipboard
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
import pyperclip

import asyncio

kb = KeyBindings()
kb.add("tab")(focus_next)
kb.add("s-tab")(focus_previous)

# Create a PyperclipClipboard instance
clipboard = PyperclipClipboard()

chat_history = []
file_to_write = False

help_text = """
Welcome !
Press Control-Q to exit.
Ctrl+C to copy text
Press Tab or Shift+Tab to navigate.


"""

@kb.add('c-q')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    utils.save_chat_history(chat_history, file_to_write)
    event.app.exit()

output_field = TextArea(style="class:output-field", text=help_text, scrollbar=True, wrap_lines=True, focus_on_click=True, read_only=True)
search_field = SearchToolbar()  # For reverse search.
input_field = TextArea(
    height=5,
    prompt=">>> ",
    style="class:input-field",
    multiline=True,
    search_field=search_field,
    focus_on_click=True,
    width=90
)

def load_history(item):
    global chat_history, file_to_write
    path_history = f"./history/{item}"
    chat_history = utils.get_chat_history(path_history)
    file_to_write = path_history
    output_field.read_only = False
    output_field.buffer.document = Document(text="History loaded\n")
    for history in chat_history:
        if history['role'] == 'user':
            output_field.buffer.insert_text(data=f"> You: {history['content']}", move_cursor=True)
            output_field.buffer.insert_line_below()
        elif history['role'] == 'assistant':
            output_field.buffer.insert_text(data=f"> GPT: {history['content']}", move_cursor=True)
            output_field.buffer.insert_line_below()
    output_field.read_only = True

def get_directory_contents(directory_path):
    try:
        return os.listdir(directory_path)
    except:
        return ['nothing here']

@kb.add("c-c")  # Ctrl+C to copy text
def copy_text(event):
    buffer = event.current_buffer  # Get the text from the buffer
    selected_text = buffer.document.text[buffer.selection_state.original_cursor_position:buffer.cursor_position]
    pyperclip.copy(selected_text)

def main():
    set_stream(choice=True)

    global chat_history

    parser = argparse.ArgumentParser(description="A ChatGPT like in CLI")
    parser.add_argument('--instruct', '-t', help='Instruct', default=False)

    args = parser.parse_args()
    if args.instruct:
        set_custom_instruction(args.instruct)
    else:
        custom_instruction = input_dialog(
            title='Custom Instructions',
            text='Please type your custom instructions:', default=utils.read_markdown_file()).run()
        set_custom_instruction(custom_instruction or "You are a helpful assistant.")
    
    items = [Button(text=item, width=40, handler=partial(load_history, item)) for item in get_directory_contents("./history")]

    container = HSplit(
        [
            VSplit([
                Box(body=HSplit(items, align="TOP"), width=40),
                Window(width=1, char='|'),
                output_field,
            ], width=1),
            Window(height=1, char="-", style="class:line"),
            input_field,
            search_field,
        ]
    )

    style = Style(
        [
            ("output-field", "bg:#000000 #27ae60"),
            ("input-field", "bg:#000000 #ffffff"),
            ("line", "#004400"),
        ]
    )

    async def print_response(response, chat_history):
        answer = ''
        output_field.buffer.insert_text(data="> GPT: ", move_cursor=True)
        for record in response:
            event_text = record['choices'][0]['delta']
            content = event_text.get('content', '')
            answer = answer + (event_text.get('content', ''))
            output_field.buffer.insert_text(data=content, move_cursor=True)
            await asyncio.sleep(0)
        assistant_message = {"role": "assistant", "content": answer}
        chat_history.append(assistant_message)
        output_field.buffer.insert_line_below()
        output_field.read_only = True

    async def accept(text_input):
        global chat_history
        output_field.buffer.cursor_position = len(output_field.buffer.text)
        output_field.read_only = False
        output_field.buffer.insert_text(data=f"> You: {text_input}", move_cursor=True)
        output_field.buffer.insert_line_below()
        log_message, response = stream_response(user_messages=text_input, chat_history=chat_history)
        chat_history = log_message
        await print_response(response, chat_history) # print response asynchronously
    
    def handle_input(buff):
        asyncio.ensure_future(accept(buff.text))

    input_field.accept_handler = handle_input

    layout = Layout(container, focused_element=input_field)

    app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, style=style, paste_mode=True, clipboard=clipboard)

    app.run()

if __name__ == "__main__":
    main()
