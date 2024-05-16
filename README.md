# bashGPT

`bashGPT` is a command-line tool that utilizes OpenAI's GPT-4 API (or a local model) to generate bash commands based on user descriptions. It can also copy the generated command to your clipboard for easy pasting.

## Features

- Generate bash commands from natural language descriptions.
- Support for both OpenAI GPT-4 API and local models.
- Copy the generated command to clipboard with a simple switch.
- Options for verbose output and complex commands separated by `&&`.

![image](https://github.com/ddxfish/bashGPT/assets/6764685/32be7ca9-5bb3-475e-840d-c838d3dfc289)


## Installation

### Requirements

Ensure you have Python installed. You can install the necessary Python packages using the `requirements.txt` file:

    pip install -r requirements.txt

### Setting Up

1. Clone the repository:  
    git clone https://github.com/ddxfish/bashGPT/  
    cd bashGPT

2. Install the dependencies:  
    pip install -r requirements.txt  

3. Create a bash script to call your Python script: (supposed to have your current directory)
    echo -e '#!/bin/bash\npython '"$(pwd)"'/bashGPT.py "$@"' > bashgpt.sh  
    chmod +x bashgpt.sh

4. Move the bash script to a directory in your PATH:  
    sudo mv bashgpt.sh /usr/local/bin/bashgpt  

5. Add your GPT-4 API key to the python script (or just use local)  
    nano main.py  

## Usage

### Command Line Arguments

- `description`: Description of the command you want to generate.
- `-t, --tokens`: Maximum number of tokens for the response. (default: 100)
- `-g, --backticks`: Wrap the output in backtick characters.
- `-l, --local`: Use the local model instead of GPT-4 API.
- `-m, --multiple`: If the action is complex, provide multiple commands separated by `&&`.
- `-v, --verbose`: Enable verbose output.
- `-c, --clipboard`: Copy the generated command to the clipboard.

### Example Usage

Generate a simple bash command:  
    bashgpt "tar the file xyz.abc" 

Generate a command with multiple steps:  
    bashgpt "set up a Python virtual environment and install dependencies" -t 500 -m

Generate a command and copy it to the clipboard:  
    bashgpt "create a new directory and navigate into it" -c

Enable verbose output to see detailed logs:  
    bashgpt "install Docker and start the service" -v

### Example Output

    Generated command:
    mkdir new_directory && cd new_directory
    Command copied to clipboard.

## Contributing

Feel free to submit issues or pull requests if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or inquiries, please contact me!
