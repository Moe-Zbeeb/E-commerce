import os

def extract_python_code(directory, output_file):
    """
    Extracts all Python code from .py files in a directory and writes to a text file.
    
    Args:
        directory (str): The path to the directory to scan for Python files.
        output_file (str): The path to the output text file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        outfile.write(f"File: {file_path}\n")
                        outfile.write("-" * 80 + "\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as pyfile:
                                outfile.write(pyfile.read())
                        except Exception as e:
                            outfile.write(f"Error reading file: {e}\n")
                        outfile.write("\n" + "=" * 80 + "\n\n")
        print(f"Python code successfully written to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

# Example usage:
directory_path = "/home/mohammad/E-commerce-1/app"
output_file_path = "extracted_code.txt"
extract_python_code(directory_path, output_file_path)
