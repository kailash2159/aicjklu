import os
import re

directory = r"c:\Users\KAILASH\Downloads\website"

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expression to match the flex gap-10 div that contains Privacy
        pattern = r'<div class="flex gap-10"[^>]*>[\s\S]*?Privacy[\s\S]*?</div>'

        if re.search(pattern, content):
            new_content = re.sub(pattern, '', content)
            
            # also remove any dangling empty lines left by this
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed privacy block from {filename}")
        else:
            print(f"No privacy block found in {filename}")
