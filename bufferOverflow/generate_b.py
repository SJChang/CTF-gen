import re

# Function to extract key components from a C file
def extract_components(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract functions
    functions = re.findall(r"(\w+)\s*\([^)]*\)\s*\{[^}]+\}", content, re.DOTALL)

    # Extract buffer declarations
    buffers = re.findall(r"char\s+\w+\s*\[\d+\];", content)

    # Extract conditional checks (e.g., strcmp)
    conditions = re.findall(r"if\s*\([^)]+\)\s*\{[^}]+\}", content, re.DOTALL)

    # Extract main function
    main_function = re.search(r"int\s+main\s*\([^)]*\)\s*\{[^}]+\}", content, re.DOTALL)
    if main_function:
        main_function = main_function.group(0)

    return {
        "functions": functions,
        "buffers": buffers,
        "conditions": conditions,
        "main_function": main_function,
    }

# Function to generate b.c based on learned components
def generate_b_c(b1_components, b2_components):
    # Combine components from b1.c and b2.c
    combined_functions = list(set(b1_components["functions"] + b2_components["functions"]))
    combined_buffers = list(set(b1_components["buffers"] + b2_components["buffers"]))
    combined_conditions = list(set(b1_components["conditions"] + b2_components["conditions"]))
    main_function = b2_components["main_function"]  # Use main function from b2.c

    # Generate b.c content
    b_c_content = """
#include <stdio.h>
#include <string.h>
// gcc -no-pie -fno-stack-protector -g -o b b.c

"""

    # Add functions
    for func in combined_functions:
        b_c_content += func + "\n\n"

    # Add main function
    b_c_content += main_function + "\n"

    return b_c_content

# Save the generated b.c to a file
def save_b_c(content, output_path):
    with open(output_path, 'w') as f:
        f.write(content)

# Main function
if __name__ == "__main__":
    # Paths to the input files
    b1_path = "b1.c"
    b2_path = "b2.c"
    output_path = "b.c"

    # Extract components from b1.c and b2.c
    b1_components = extract_components(b1_path)
    b2_components = extract_components(b2_path)

    # Generate b.c
    b_c_content = generate_b_c(b1_components, b2_components)

    # Save the generated b.c
    save_b_c(b_c_content, output_path)

    print(f"Generated {output_path} successfully!")