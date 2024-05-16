import argparse
import openai
import requests
import json
import sys
import os
import pyperclip

# Constants
api_key = os.getenv('bashGPT4_API_KEY') # set this environment variable for security
if not api_key:
    # Use a hardcoded fallback if no input is provided
    api_key = 'YOUR_API_KEY_HERE'  # You should ideally have this as a last resort or removed entirely for security reasons

def generate_base_description(description, multiple_commands, cmdorscript):
    base_description = f"Generate a bash {cmdorscript} to: {description}."
    if multiple_commands:
        base_description += f" If this is a complex action, provide multiple {cmdorscript}s separated by '&&'."
    return base_description

# Function to query GPT-4 API
def query_gpt4(max_tokens, use_backticks, description, multiple_commands, verbose, cmdorscript):
    try:
        openai.api_key = api_key
        client = openai.ChatCompletion()

        messages = [
            {"role": "system", "content": f"You are an assistant skilled in generating bash {cmdorscript}s based on user descriptions. No markup. No description, just the {cmdorscript}."},
            {"role": "user", "content": generate_base_description(description, multiple_commands, cmdorscript)}
        ]

        if verbose:
            print("Sending request to GPT-4 API...")
        response = client.create(
            model="gpt-4",
            messages=messages,
            max_tokens=max_tokens,
        )
        if verbose:
            print("Received response from GPT-4 API.")

        command = response.choices[0].message['content'].strip()
        if use_backticks:
            command = f"`{command}`"
        return command

    except Exception as e:
        if verbose:
            print(f"Error querying GPT-4 API: {e}")
        return None

# Function to query local model
def query_local_model(max_tokens, use_backticks, description, multiple_commands, verbose, cmdorscript):
    try:
        url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        data = {
            "model": "model-identifier",
            "messages": [
                {"role": "system", "content": f"You are an assistant skilled in generating bash {cmdorscript}s based on user descriptions. No markup. No description, just the {cmdorscript}."},
                {"role": "user", "content": generate_base_description(description, multiple_commands, cmdorscript)}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens if max_tokens > 0 else -1,
            "stream": False
        }

        if verbose:
            print("Sending request to local model...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if verbose:
            print("Received response from local model.")

        response_json = response.json()
        command = response_json['choices'][0]['message']['content'].strip()
        if use_backticks:
            command = f"`{command}`"
        return command

    except Exception as e:
        if verbose:
            print(f"Error querying local model: {e}")
        return None

# Command-line interface
def main():
    parser = argparse.ArgumentParser(
        description="Query GPT-4 or a local model to generate a bash command.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('description', type=str, nargs='+', help="Description of the command you want to generate.")
    parser.add_argument('-t', '--tokens', type=int, default=100, help="Maximum number of tokens for the response.")
    parser.add_argument('-g', '--backticks', action='store_true', help="Wrap the output in backtick characters.")
    parser.add_argument('-l', '--local', action='store_true', help="Use the local LM Studio model instead of GPT-4 API.")
    parser.add_argument('-m', '--multiple', action='store_true', help="If the action is complex, provide multiple commands separated by '&&'.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    parser.add_argument('-c', '--clipboard', action='store_true', help="Copy the generated command to the clipboard.")
    parser.add_argument('-s', '--script', action='store_true', help="Generate a script instead of a command.")


    args = parser.parse_args()
    
    # Combine description arguments into a single string
    description = ' '.join(args.description)

    cmdorscript = "script" if args.script else "command"

    if not description:
        parser.print_help()
        sys.exit(1)

    if args.local:
        command = query_local_model(args.tokens, args.backticks, description, args.multiple, args.verbose, cmdorscript)
    else:
        command = query_gpt4(args.tokens, args.backticks, description, args.multiple, args.verbose, cmdorscript)

    if command:
        if args.verbose: print("Generated command:")
        print(command)
        if args.backticks:
            command = f"`{command}`"
        if args.clipboard:
            pyperclip.copy(command)
            print("##Command copied to clipboard.")
    else:
        print("Failed to generate command.")

if __name__ == "__main__":
    main()