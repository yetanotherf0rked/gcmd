#!/usr/bin/env python3

import platform
import os
import sys
import getpass
import distro
import shutil
import subprocess
from openai import OpenAI
from simple_term_menu import TerminalMenu
import pyperclip

api_key = os.getenv("OPENAI_GPT_CMD_API_KEY")
MODEL = "gpt-4"
client = OpenAI(api_key=api_key)
PROMPT = """
You’re a command-line assistant. You provide users with command lines that answer their request.

Each line of your response to the request must be single-line command solutions formatted as:
[Command-line] # Short Description if necessary

Do not add any explanations beyond the formatted responses.

User Request: [USER_PROMPT]
User OS details: [SYS_INFO]
"""

def get_system_info():
    system_info = {
        "OS Type": platform.system(),
        "OS Version": platform.version(),
        "OS Release": platform.release(),
        "Machine": platform.machine(),
        "Architecture": platform.architecture()[0],
        "User Privileges": "Root" if os.geteuid() == 0 else "Regular User",
    }

    # Get distribution info on Linux
    if system_info["OS Type"] == "Linux":
        system_info.update({
            "Distro Name": distro.name(pretty=True),
            "Distro Version": distro.version(),
            "Distro ID": distro.id(),
        })
    elif system_info["OS Type"] == "Darwin":
        system_info["Distro Name"] = "macOS"

    # Detect the shell and version
    system_info["Shell"], system_info["Shell Version"] = detect_shell()

    # Determine if Python has admin privileges
    system_info["Privileges"] = "Admin" if is_admin() else "Non-Admin"

    return system_info

def detect_shell():
    """Detect the current shell and version."""
    shell = os.getenv("SHELL") or os.getenv("COMSPEC", "")
    shell_name = os.path.basename(shell)
    try:
        shell_version = subprocess.check_output([shell_name, "--version"], text=True).splitlines()[0]
    except Exception:
        shell_version = "Unknown"
    return shell_name, shell_version

def is_admin():
    """Check if the current user has admin (root) privileges."""
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Windows doesn't have os.geteuid; fallback for Windows (not tested)
        return ctypes.windll.shell32.IsUserAnAdmin() != 0 if sys.platform == "win32" else False

def display_system_info():
    """Print system information in a user-friendly way."""
    info = get_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")

def load_prompt_template(command_question):
    """Load prompt template and insert request."""
    return PROMPT.replace("[USER_PROMPT]", command_question).replace("[SYS_INFO]",str(get_system_info())) 

def get_gpt_command_response(prompt):
    """Send the structured prompt to OpenAI API and retrieve the response."""
    try:
        response = client.chat.completions.create(model=MODEL,
        messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content
    except Exception as e:
        print("Error connecting to the OpenAI API:", e)
        sys.exit(1)

def parse_response_into_options(response):
    """Parse GPT response into options, combining solution and command as one entry."""
    return [line for line in response.splitlines() if line.strip()]

def display_menu_and_select(options):
    """Display solutions in a menu and allow the user to select one."""
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index is not None:
        selected_command = options[menu_entry_index]
        return selected_command
    else:
        print("No command selected.")
        sys.exit(0)

def main():
    # Check that user provided a command question
    if len(sys.argv) < 2:
        print("Usage: gpt-cmd <prompt>")
        sys.exit(1)

    command_question = sys.argv[1]

    # Load structured prompt from prompt.txt and insert the command question
    prompt = load_prompt_template(command_question)
    response = get_gpt_command_response(prompt)

    # Parse the GPT Command response into options for menu display
    options = parse_response_into_options(response)

    if not options:
        print("No solutions found.")
        sys.exit(1)

    # Display menu and select command
    selected_command = display_menu_and_select(options)
    pyperclip.copy(selected_command)
    print(f"{selected_command} (Command copied to clipboard)")

if __name__ == "__main__":
    main()

