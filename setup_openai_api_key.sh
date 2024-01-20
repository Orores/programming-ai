#!/bin/bash

ENV_FILE=".env"
KEY_NAME="OPENAI_API_KEY"

# Function to ask for API key and write to .env file
write_api_key() {
    echo "Please enter your OpenAI API key:"
    read -r OPENAI_API_KEY
    echo "$KEY_NAME=$OPENAI_API_KEY" > "$ENV_FILE"
    echo "API key written to $ENV_FILE"
}

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
    # Check if OPENAI_API_KEY is set in .env
    if grep -q "$KEY_NAME" "$ENV_FILE"; then
        echo "API key already exists in $ENV_FILE."
        echo "Do you want to overwrite it? [y/n]"
        read -r response

        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            write_api_key
        else
            echo "API key remains unchanged."
        fi
    else
        echo "No API key found in $ENV_FILE."
        write_api_key
    fi
else
    echo "No .env file found. Creating one now..."
    write_api_key
fi

