import os
import re

# USAGE: Cleans SQLCMD exports by removing the dashed separator line (2nd line).
# 1. Automatically detects encoding (UTF-8, CP1252, etc.) to prevent crash on special characters.
# 2. Identifies and deletes the "-------|-------" formatting line.
# 3. Re-saves the file as clean UTF-8 for better compatibility with modern apps.

def remove_separator_lines():
    # Get all csv files in the current directory
    files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]

    if not files:
        print("No CSV files found in the current directory.")
        return

    # Common encodings for SQL exports
    encodings_to_try = ['utf-8', 'cp1252', 'latin-1', 'utf-16']

    for file_path in files:
        content = None
        used_encoding = None

        # 1. ATTEMPT TO READ WITH VARIOUS ENCODINGS
        for enc in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.readlines()
                used_encoding = enc
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if content is None:
            print(f"Could not decode {file_path}. Skipping.")
            continue

        if len(content) < 2:
            continue

        # 2. PROCESS AND REMOVE SEPARATOR
        print(f"Processing: {file_path} (Detected: {used_encoding})")

        new_content = []
        for index, line in enumerate(content):
            # Regex targets lines that are just dashes, pipes, and whitespace
            is_separator = re.match(r'^[ \-\|]+$', line.strip())

            # Skip if it's the second line and matches the pattern
            if index == 1 and is_separator:
                continue

            new_content.append(line)

        # 3. WRITE BACK (Saving as UTF-8 for better future compatibility)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_content)
        except Exception as e:
            print(f"Error writing {file_path}: {e}")

    print("\nCleanup complete.")

if __name__ == "__main__":
    remove_separator_lines()
