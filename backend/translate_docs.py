import os
import re
from pathlib import Path
from deep_translator import GoogleTranslator
import time

# Config
SOURCE_DIR = Path("../docusaurus-root/docs")
TARGET_DIR = Path("../docusaurus-root/i18n/ur/docusaurus-plugin-content-docs/current")

# Initialize Translator
def get_translator():
    return GoogleTranslator(source='auto', target='ur')

def translate_text(text):
    if not text.strip():
        return text
    try:
        # Deep Translator is synchronous
        translator = get_translator()
        result = translator.translate(text)
        return result
    except Exception as e:
        print(f"Error translating text: {e}")
        # Add a small delay and retry once
        try:
            time.sleep(1)
            translator = get_translator()
            result = translator.translate(text)
            return result
        except:
            return text

def is_code_block_start(line):
    return line.strip().startswith("```")

def translate_markdown_file(source_path, target_path):
    print(f"Translating {source_path.name}...")
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter
    parts = content.split('---', 2)
    
    new_content = ""
    
    if len(parts) >= 3:
        # Has frontmatter
        frontmatter = parts[1]
        body = parts[2]
        
        # Process frontmatter lines (title, description)
        new_frontmatter = []
        for line in frontmatter.strip().split('\n'):
            if line.startswith('title:') or line.startswith('description:'):
                key, val = line.split(':', 1)
                trans_val = translate_text(val.strip())
                new_frontmatter.append(f"{key}: {trans_val}")
            else:
                new_frontmatter.append(line)
        
        joined_frontmatter = '\n'.join(new_frontmatter)
        new_content += f"---\n{joined_frontmatter}\n---\n"
    else:
        body = content

    # Process Body
    lines = body.split('\n')
    in_code_block = False
    
    new_body_lines = []
    
    for line in lines:
        if is_code_block_start(line):
            in_code_block = not in_code_block
            new_body_lines.append(line)
            continue
            
        if in_code_block:
            # Don't translate code
            new_body_lines.append(line)
            continue
            
        # Check for special markdown elements to skip/handle carefully
        stripped = line.strip()
        if stripped == '' or stripped.startswith(('import ', 'export ', '<', ':::')):
            new_body_lines.append(line)
            continue
            
        # Headers
        if stripped.startswith('#'):
            level = len(line.split(' ')[0])
            text = line[level:].strip()
            trans = translate_text(text)
            new_body_lines.append(f"{'#' * level} {trans}")
            continue
            
        # Simple heuristic: If line has little markdown, translate it
        if not re.search(r'\]\(|<|:::|```', line):
            trans = translate_text(line)
            new_body_lines.append(trans)
        else:
            # For complex lines, try to translate but fallback to original
            try:
                trans = translate_text(line)
                new_body_lines.append(trans)
            except:
                new_body_lines.append(line)

    new_content += '\n'.join(new_body_lines)

    # Ensure target directory exists
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Saved to {target_path}")

def main():
    if not SOURCE_DIR.exists():
        print(f"Source dir {SOURCE_DIR} not found!")
        return

    # Walk through source directory
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                source_file = Path(root) / file
                
                # Compute relative path to maintain structure
                try:
                    rel_path = source_file.relative_to(SOURCE_DIR)
                except ValueError:
                    continue 

                target_file = TARGET_DIR / rel_path
                
                translate_markdown_file(source_file, target_file)

    print("\n✅ All documents translated!")

if __name__ == "__main__":
    main()
