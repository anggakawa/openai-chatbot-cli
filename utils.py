import os
import json

def save_chat_history(chat_history, output_file="chat_history.json"):
    import json
    with open(output_file, "w") as file:
        json.dump(chat_history, file)

def print_output(output_file, response):
    with open(output_file, 'w') as output_file:
        output_file.write(response)

def get_chat_history(input):
    # Load existing chat history from a JSON file if provided
    chat_history = []
    if os.path.exists(input):
        with open(input, "r") as file:
            file_contents = file.read()  # Read the file contents
            if file_contents:  # Check if the file is not empty
                loaded_data = json.loads(file_contents)  # Load the JSON data
                if loaded_data:
                    chat_history = loaded_data
                else:
                    print("The file exists, but it doesn't contain any chat history data.")
            else:
                print("The file is empty.")
    return chat_history