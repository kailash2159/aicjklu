import os
import re

directory = r"c:\Users\KAILASH\Downloads\website"
index_file = os.path.join(directory, "index.html")

# Read index.html to extract the latest navbar
with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

nav_match = re.search(r'<!-- Navigation -->\s*<nav[^>]*>.*?</nav>', index_content, flags=re.DOTALL | re.IGNORECASE)
if not nav_match:
    print("Could not find navbar in index.html")
    exit(1)

nav_html = nav_match.group(0)

# Files to update
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the existing navbar
    new_content = re.sub(r'<!--\s*Navigation\s*-->\s*<nav[^>]*>.*?</nav>', nav_html, content, flags=re.DOTALL | re.IGNORECASE)
    
    # In case the comment is missing but <nav> exists
    if new_content == content:
        new_content = re.sub(r'<nav[^>]*>.*?</nav>', nav_html, content, flags=re.DOTALL | re.IGNORECASE, count=1)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"Skipped {filename} (no navbar found)")

print("Done updating navbars.")
