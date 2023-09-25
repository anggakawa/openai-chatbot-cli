import argparse
from openai_utils import create_chat_response, set_custom_instruction, set_stream
import utils
from rich.prompt import Prompt
from rich.console import Console
from prompt_toolkit import prompt

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="A simple command-line program")
    
    # Add command-line arguments
    parser.add_argument('--chat', '-c', help='Chat')
    parser.add_argument('--instruct', '-t', help='Instruct', default=False)
    parser.add_argument('--input', '-i', help='Input file', default=False)
    parser.add_argument('--output', '-o', help='Output file', default='output.md')
    parser.add_argument('-s', action="store_true", help='Stream')
    parser.add_argument('-p', action="store_true", help='Prompt mode')
    
    chat = ''

    args = parser.parse_args()

    # Load existing chat history from a JSON file if provided
    chat_history = utils.get_chat_history(args.input)

    if args.instruct:
        set_custom_instruction(args.instruct)
    
    if args.s:
        set_stream(choice=True)

    if args.p:
        response = ''
        console.print("Welcome to Chatbot CLI Tool, type `\q` to quit", markup=True)
        while True:
            # chat = Prompt.ask("Enter your prompt", default="Hello")
            chat = prompt("Enter your prompt: ", multiline=True)
            if chat == '\q':
                break
            chat_history, response = create_chat_response(user_messages=chat, chat_history=chat_history)
    elif args.chat:
        chat = args.chat
        # Create chat response and update chat history
        chat_history, response = create_chat_response(user_messages=chat, chat_history=chat_history)
    else:
        console.print("You need to include `--chat` or `-p` to use the app!", markup=True)
        return

    # Save chat history to a JSON file
    utils.save_chat_history(chat_history, args.input)
    utils.print_output(args.output, response)

if __name__ == "__main__":
    main()
