# Chatbot CLI Tool

This is a simple command-line program for interacting with a chatbot powered by OpenAI's GPT. You can use this tool to have conversations with the chatbot, customize its behavior with instructions, and save chat history.

# Usage
![Usage Tutorial](<assets/tutorial.gif>)

## Preparation
To configure this tool and manage sensitive information, you can use environment variables. Create a `.env` file in the root directory of your project and add the following variables:

```dotenv
OPENAI_API_KEY=YOURKEY
OPENAI_ORG=YOURORG
```

## Basic Usage
To run the chatbot CLI tool, use the following command:

```bash
python main.py
```

Optional Arguments
- `--instruct/-t`: Specify custom instructions for the chatbot. (Optional), if not specified you will get an input dialog asking for custom instructions, you can choose `<cancel>`


## Custom Instructions
You can provide custom instructions to the chatbot using the --instruct option. For example:

```bash
python main.py --instruct "Generate a funny response"
```

## Loading Existing Chat History

If you have an existing chat history stored in a JSON file, the tool will load it when you select the chat, if not it will create a new chat history.



