import argparse
from openai_utils import create_chat_response, set_custom_instruction, set_stream
import utils

def main():
    parser = argparse.ArgumentParser(description="A simple command-line program")
    
    # Add command-line arguments
    parser.add_argument('--chat', '-c', help='Chat', required=True)
    parser.add_argument('--instruct', '-t', help='Instruct', default=False)
    parser.add_argument('--input', '-i', help='Input file', default='chat_history.json')
    parser.add_argument('--output', '-o', help='Output file', default='output.md')
    parser.add_argument('-s', action="store_true", help='Stream')
    
    args = parser.parse_args()

    if args.instruct:
        set_custom_instruction(args.instruct)
    
    if args.s:
        set_stream(choice=True)

    # Load existing chat history from a JSON file if provided
    chat_history = utils.get_chat_history(args.input)

    # Create chat response and update chat history
    chat_history, response = create_chat_response(user_messages=args.chat, chat_history=chat_history)

    # Save chat history to a JSON file
    utils.save_chat_history(chat_history, args.input)
    utils.print_output(args.output, response)

if __name__ == "__main__":
    main()
