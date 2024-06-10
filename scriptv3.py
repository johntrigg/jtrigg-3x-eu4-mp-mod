import os
import shutil
from config import directories_to_modify, search_terms  # Importing the arrays from config.py

# Flag to determine if the original file should be modified
modify_original = True

def read_file_with_multiple_encodings(file_path, encodings=['utf-8', 'ascii', 'latin1']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.readlines(), encoding
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    raise UnicodeDecodeError(f"Cannot decode file: {file_path}")

# Process each directory in the list
for directory in directories_to_modify:
    # Ensure the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Check if the file is a .txt file
            if filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                
                try:
                    # Read the content of the file with multiple encodings
                    content, used_encoding = read_file_with_multiple_encodings(file_path)
                    print(f"Successfully read file '{file_path}' with encoding '{used_encoding}'")
                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError while reading file '{file_path}': {e}")
                    continue

                # Modify the required lines
                for i, line in enumerate(content):
                    for term in search_terms:
                        if term in line:
                            try:
                                # Split line by '=' to separate key and value, handle comments
                                parts = line.split('=')
                                if len(parts) >= 2:
                                    # Handle comments
                                    value_part = parts[1].split('#')[0].strip()
                                    value = float(value_part)
                                    # Tripling the value and rounding to two decimal places
                                    new_value = round(value * 3, 2)
                                    # Replacing the value in the line, preserving comments
                                    comment = '#' + parts[1].split('#')[1] if '#' in parts[1] else ''
                                    content[i] = f'{parts[0]}= {new_value} {comment}\n'
                            except ValueError:
                                # If the value is not a float, do nothing
                                pass
                            except Exception as e:
                                # Print the modifier and file that caused the issue
                                print(f"Error processing term '{term}' in file '{file_path}': {e}")

                # Creating the output file name
                output_filename = f'{os.path.splitext(filename)[0]}Modified3TimesModifiers.txt'
                output_path = os.path.join(directory, output_filename)
                
                try:
                    # Writing the modified lines to the new file
                    with open(output_path, 'w', encoding='utf-8') as file:
                        file.writelines(content)
                except Exception as e:
                    print(f"Error writing to file '{output_path}': {e}")
                    continue

                # Replace the original file with the modified version if the flag is set
                if modify_original:
                    try:
                        shutil.move(output_path, file_path)
                    except Exception as e:
                        print(f"Error replacing the original file '{file_path}' with '{output_path}': {e}")
                else:
                    try:
                        shutil.copy(output_path, os.path.join(directory, 'output.txt'))
                    except Exception as e:
                        print(f"Error copying the file '{output_path}' to output.txt: {e}")

print("The values have been updated successfully in all .txt files in the specified directories.")

# Additional part to modify specific values in 00_static_modifiers.txt

# Specific file and terms to modify
specific_file_path = r'C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\static_modifiers\00_static_modifiers.txt'
specific_terms = {
    "local_state_maintenance_modifier": 0.1,
    "local_monthly_devastation": -0.05,
    "local_unrest": -3,
    "local_manpower_modifier": 0.33
}

def triple_specific_values(file_path, terms):
    try:
        content, used_encoding = read_file_with_multiple_encodings(file_path)
        print(f"Successfully read specific file '{file_path}' with encoding '{used_encoding}'")
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError while reading specific file '{file_path}': {e}")
        return

    in_relevant_block = False
    for i, line in enumerate(content):
        if 'patriarch_state' in line or 'patriarch_authority_local' in line:
            in_relevant_block = True
        if in_relevant_block and '}' in line:
            in_relevant_block = False

        if in_relevant_block:
            for term, original_value in terms.items():
                if term in line:
                    try:
                        # Triple the specific value
                        new_value = round(original_value * 3, 2)
                        # Split line by '=' to separate key and value, handle comments
                        parts = line.split('=')
                        if len(parts) >= 2:
                            # Replacing the value in the line, preserving comments
                            comment = '#' + parts[1].split('#')[1] if '#' in parts[1] else ''
                            content[i] = f'{parts[0]}= {new_value} {comment}\n'
                    except Exception as e:
                        print(f"Error processing term '{term}' in specific file '{file_path}': {e}")

    # Writing the modified lines to the new file
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(content)
        print(f"Successfully modified specific file '{file_path}'")
    except Exception as e:
        print(f"Error writing to specific file '{file_path}': {e}")

# Call the function to modify the specific values
triple_specific_values(specific_file_path, specific_terms)
