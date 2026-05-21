import os

directory = r"c:\Users\KAILASH\Downloads\website"
index_file = os.path.join(directory, "index.html")

def extract_navbar(content):
    content_lower = content.lower()
    # Find start comment or start of nav tag
    start_comment = content_lower.find("<!-- navigation -->")
    if start_comment == -1:
        start_comment = content_lower.find("<!--navigation-->")
    
    if start_comment == -1:
        start_pos = content_lower.find("<nav")
    else:
        start_pos = content_lower.find("<nav", start_comment)
        
    if start_pos == -1:
        return None
        
    # Count nesting of <nav> and </nav> tags
    pos = start_pos + 4
    count = 1
    while count > 0 and pos < len(content):
        next_open = content_lower.find("<nav", pos)
        next_close = content_lower.find("</nav>", pos)
        
        if next_open == -1 and next_close == -1:
            break
        if next_open != -1 and (next_close == -1 or next_open < next_close):
            count += 1
            pos = next_open + 4
        else:
            count -= 1
            pos = next_close + 6
            
    if count == 0:
        actual_start = start_comment if start_comment != -1 else start_pos
        return content[actual_start:pos]
    return None

# Read index.html to extract the latest navbar
with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

nav_html = extract_navbar(index_content)
if not nav_html:
    print("Could not find navbar in index.html")
    exit(1)

# Files to update
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    target_nav = extract_navbar(content)
    if target_nav and target_nav != nav_html:
        new_content = content.replace(target_nav, nav_html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    elif target_nav == nav_html:
        print(f"Skipped {filename} (navbar already up to date)")
    else:
        print(f"Skipped {filename} (no navbar found)")

print("Done updating navbars.")
