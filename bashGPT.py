import argparse
import openai
import requests
import json
import sys
import pyperclip

# Function to query GPT-4 API
def query_gpt4(max_tokens, use_backticks, description, multiple_commands, verbose):
    try:
        openai.api_key = 'YOUR API KEY FOR GPT4'  # Replace with your OpenAI API key

        client = openai.ChatCompletion()

        # Base description with the instruction to generate a bash command
        base_description = f"Generate a bash command to: {description}."
        
        # Adjust the description if multiple commands are requested
        if multiple_commands:
            base_description += " If this is a complex action, provide multiple commands separated by '&&'."

        messages = [
            {"role": "system", "content": "You are an assistant skilled in generating bash commands based on user descriptions. No markup. No descrition, just the command."},
            {"role": "user", "content": base_description}
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

# Function to query local model -- this uses LM Studio instead of GPT 4
def query_local_model(max_tokens, use_backticks, description, multiple_commands, verbose):
    try:
        url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        # Base description with the instruction to generate a bash command
        base_description = f"Generate a bash command to: {description}."
        
        # Adjust the description if multiple commands are requested
        if multiple_commands:
            base_description += " If this is a complex action, provide multiple commands separated by '&&'."

        data = {
            "model": "model-identifier",
            "messages": [
                {"role": "system", "content": "You are an assistant skilled in generating bash commands based on user descriptions. No markup. No descrition, just the command."},
                {"role": "user", "content": base_description}
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
    parser.add_argument('description', type=str, nargs='?', help="Description of the command you want to generate.")
    parser.add_argument('-t', '--tokens', type=int, default=100, help="Maximum number of tokens for the response.")
    parser.add_argument('-g', '--backticks', action='store_true', help="Wrap the output in backtick characters.")
    parser.add_argument('-l', '--local', action='store_true', help="Use the local LM Studio (similar to openapi) model instead of GPT-4 API.")
    parser.add_argument('-m', '--multiple', action='store_true', help="If the action is complex, provide multiple commands separated by '&&'.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    parser.add_argument('-c', '--clipboard', action='store_true', help="Copy the generated command to the clipboard.")

    args = parser.parse_args()

    if args.description is None:
        parser.print_help()
        sys.exit(1)

    if args.local:
        command = query_local_model(args.tokens, args.backticks, args.description, args.multiple, args.verbose)
    else:
        command = query_gpt4(args.tokens, args.backticks, args.description, args.multiple, args.verbose)

    if command:
        print("Generated command:")
        print(command)
        if args.clipboard:
            pyperclip.copy(command)
            print("Command copied to clipboard.")
    else:
        print("Failed to generate command.")

if __name__ == "__main__":
    main()
