from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = "gpt-4-0613"
CUSTOM_INSTRUCTIONS = "You are a helpful assistant."

def set_custom_instruction(instructions):
    global CUSTOM_INSTRUCTIONS
    CUSTOM_INSTRUCTIONS = instructions

def list_openai_models():
    models = openai.Model.list()
    return models

def create_chat_response(user_messages="", chat_history=None):
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
        messages=log_messages
    )

    # Add assistant's reply to the log_messages
    assistant_message = {"role": "assistant", "content": response.choices[0].message.content}
    log_messages.append(assistant_message)

    return log_messages, response

def save_chat_history(chat_history, output_file="chat_history.json"):
    import json
    with open(output_file, "w") as file:
        json.dump(chat_history, file)