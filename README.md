# Chatbot CLI Tool

This is a simple command-line program for interacting with a chatbot powered by OpenAI's GPT. You can use this tool to have conversations with the chatbot, customize its behavior with instructions, and save chat history.

# Usage

## Preparation
To configure this tool and manage sensitive information, you can use environment variables. Create a `.env` file in the root directory of your project and add the following variables:

```dotenv
OPENAI_API_KEY=YOURKEY
OPENAI_ORG=YOURORG
```

## Basic Usage
To run the chatbot CLI tool, use the following command:

```bash
python main.py --chat "Your message here"
```

Replace "Your message here" with the message you want to send to the chatbot.


Optional Arguments
- `--instruct/-t`: Specify custom instructions for the chatbot. (Optional)
- `--input/-i`: Specify the input JSON file for chat history. (Default: chat_history.json)
- `--output/-o`: Specify the output file for chat responses. (Default: output.md)
- `-s`: Specify to use stream option. (Default: False)


## Custom Instructions
You can provide custom instructions to the chatbot using the --instruct option. For example:

```bash
python main.py --chat "Tell me a joke" --instruct "Generate a funny response"
```

## Loading Existing Chat History

If you have an existing chat history stored in a JSON file, the tool will load it when you run the script. If the file doesn't exist or is empty, it will create a new chat history. Use the `--input` parameter to specify.



