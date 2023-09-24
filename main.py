import argparse
from openai_utils import list_openai_models, create_chat_response, save_chat_history, set_custom_instruction
import os
import json
import markdown
import html2text

def main():
    parser = argparse.ArgumentParser(description="A simple command-line program")
    
    # Add command-line arguments
    parser.add_argument('--chat', '-c', help='Chat', required=True)
    parser.add_argument('--instruct', '-t', help='Instruct', default=False)
    parser.add_argument('--input', '-i', help='Input file', default='chat_history.json')
    parser.add_argument('--output', '-o', help='Output file', default='output.md')
    
    args = parser.parse_args()

    if args.instruct:
        set_custom_instruction(args.instruct)

    # Load existing chat history from a JSON file if provided
    chat_history = []
    if os.path.exists(args.input):
        with open(args.input, "r") as file:
            file_contents = file.read()  # Read the file contents
            if file_contents:  # Check if the file is not empty
                loaded_data = json.loads(file_contents)  # Load the JSON data
                if loaded_data:
                    chat_history = loaded_data
                else:
                    print("The file exists, but it doesn't contain any chat history data.")
            else:
                print("The file is empty.")

    # Create chat response and update chat history
    chat_history, response = create_chat_response(user_messages=args.chat, chat_history=chat_history)

    # Save chat history to a JSON file
    save_chat_history(chat_history, args.input)

    with open(args.output, 'w') as output_file:
        output_file.write(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
