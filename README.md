# gcmd: GPT Command-Line Assistant

A Python-based command-line tool that interacts with OpenAI's GPT-4 to generate and execute command-line solutions based on user input.

## Features
- Receives user requests and returns command-line solutions.
- Allows quick copy-to-clipboard functionality.
- Uses an interactive terminal menu for seamless navigation.

## Prerequisites
1. Python 3.6 or later
2. An OpenAI API key. Set it as an environment variable named `OPENAI_GPT_CMD_API_KEY`.

## Installation

1. **Clone this repository**

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the environment variable for the OpenAI API key**:
    ```bash
    export OPENAI_GPT_CMD_API_KEY="your_openai_api_key"
    ```

## Usage

```bash
python gpt-cmd.py "Your prompt"
```

## License
WTFPL
