import os
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("Anthropic API key not found in environment variables.")


directory_path = os.path.dirname(os.path.abspath(__file__))


base_file_name = 'message'
output_file = 'message_all.txt'
output_file_path = os.path.join(directory_path, output_file)

# Initialise
combined_content = ""

# Loop through files in the directory
i = 0
while True:
    # Construct the file name
    if i == 0:
        file_name = f"{base_file_name}.txt"  # message.txt
    else:
        file_name = f"{base_file_name}({i}).txt"  # message(1).txt, message(2).txt, etc.

    file_path = os.path.join(directory_path, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        break  # Exit the loop if the file doesn't exist

    # Read the contents of the file
    with open(file_path, 'r') as f:
        file_content = f.read()

    combined_content += f"File: {file_name}\n{file_content}\n\n"

    i += 1

if not combined_content:
    raise FileNotFoundError(f"No files matching '{base_file_name}*.txt' found in the directory.")

# Initialise
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Define the prompt for the LLM
prompt = f"""
You are an expert in cryptography. Below are multiple files containing cryptographic messages or challenges:

{combined_content}

Analyze these files to understand their cryptographic patterns, encoding, or encryption methods. Then, generate a new cryptographic challenge or message that follows the same style and complexity. The new challenge should:
1. Be of the same type (e.g., substitution cipher, XOR encryption, base64 encoding, etc.).
2. Include a clear description of the challenge or task.
3. Be saved in a single file named "message_all.txt".

Provide only the content for the new challenge, without any additional explanation or text.
"""

# Send the prompt to the Anthropic API
response = client.messages.create(
    model="claude-3-opus-20240229",  
    max_tokens=4000, 
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Extract the generated content from the response
generated_content = response.content[0].text

# Write the generated content to the new file
with open(output_file_path, 'w') as output_f:
    output_f.write(generated_content)

print(f"New cryptographic challenge has been generated and saved to '{output_file}'.")