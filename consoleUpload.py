# AI Retro Console with LLM, Python and N8N
# Roni Bandini, @ronibandini
# v1.0 July 2025 MIT License

import requests
import uuid
import datetime
import sys
import time
import os
import subprocess
import pyfiglet

# Settings
WEBHOOK_URL = 'https://....'
LOG_FILE = 'log.txt'
TYPE_DELAY=0.3

# Clean screen and print banner
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("AI Retro Console")
    print(banner)
    print("v1.0 7.2025 - Roni Bandini - 'quit'to exit.\n")

# Typewriter effect for AI output
def typewriter(text, delay=TYPE_DELAY):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    clear_screen()
    # Session ID for Agent Memory  
    session_id = str(uuid.uuid4())  

    while True:
        myPrompt = input("$: ")

        if myPrompt.lower() == "quit":
            print("Closing...")
            break

        params = {
            "sessionId": session_id,
            "prompt": myPrompt
        }

        try:
            response = requests.get(WEBHOOK_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if 'output' in data:
                output = data['output']
                print("AI→ ", end="", flush=True)
                typewriter(output, delay=0.02)

                if output.strip().startswith('$'):
                	# Remove leading '$'
                    command = output.strip()[1:].strip()  
                    print(f"\n[Executing command: {command}]\n")
                    try:
                        # Execute and capture output
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        if result.stdout:
                            print(result.stdout)
                        if result.stderr:
                            print("Error:", result.stderr)
                    except Exception as e:
                        print("Command execution failed:", e)
            else:
                output = str(data)
                print("Unexpected response :(", output)

            # Save log
            timestamp = datetime.datetime.now().isoformat()
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}]\nPrompt: {myPrompt}\nResponse: {output}\n\n")

        except requests.exceptions.RequestException as e:
            print("Error :( ", e)
        except ValueError:
            print("Invalid JSON :(")

if __name__ == "__main__":
    main()
