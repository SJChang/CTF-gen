import os
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("Anthropic API key not found in environment variables.")

directory_path = os.path.dirname(os.path.abspath(__file__))

# Define the sample folder
sample_folder = 'sample'
sample_folder_path = os.path.join(directory_path, sample_folder)

# All learning file is named as vuln(i).c
base_file_name = 'vuln'
output_folder = 'new code'
output_folder_path = os.path.join(directory_path, output_folder)

# Create the 'new code' folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Initialise an empty string to store combined content
combined_content = ""

# Loop through files in the sample folder
i = 0
while True:
    if i == 0:
        file_name = f"{base_file_name}.c"  # vuln.c
    else:
        file_name = f"{base_file_name}({i}).c"  # vuln(1).c, vuln(2).c, etc.

    file_path = os.path.join(sample_folder_path, file_name)

    if not os.path.exists(file_path):
        break  # Exit the loop if the file doesn't exist

    # Read the contents of the file
    with open(file_path, 'r') as f:
        file_content = f.read()

    # Append the file content to the combined content
    combined_content += f"File: {file_name}\n{file_content}\n\n"

    i += 1

if not combined_content:
    raise FileNotFoundError(f"No files matching '{base_file_name}*.c' found in the '{sample_folder}' folder.")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Define the prompt for the LLM
prompt = f"""
You are an expert in cybersecurity and CTF challenges. Below are multiple C code files that contain CTF-style buffer overflow challenges:

{combined_content}

Analyze these files to understand their purpose, structure, and the type of buffer overflow vulnerabilities they demonstrate. Then, generate a new, similar buffer overflow challenge in C code. The new challenge should:
1. Be of the same type (e.g., stack-based buffer overflow).
2. Include a vulnerability that is realistic and exploitable.
3. Include comments explaining the vulnerability and how it can be exploited.
4. Be saved in a single file named "vuln_all.c".

Provide only the C code for the new challenge, without any additional explanation or text.
"""

response = client.messages.create(
    model="claude-3-opus-20240229", 
    max_tokens=4000, 
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Extract the generated content from the response
generated_content = response.content[0].text

# Determine the new file name
i = 1
while True:
    new_file_name = f"vuln_new_{i}.c"
    new_file_path = os.path.join(output_folder_path, new_file_name)
    if not os.path.exists(new_file_path):
        break
    i += 1

# Write the generated content to the new file
with open(new_file_path, 'w') as output_f:
    output_f.write(generated_content)

print(f"New buffer overflow challenge has been generated and saved to '{new_file_path}'.")