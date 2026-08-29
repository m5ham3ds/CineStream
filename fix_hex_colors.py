import os
import re

skip_files = ['Theme.kt', 'Color.kt']

def process_file(filepath):
    filename = os.path.basename(filepath)
    if filename in skip_files:
        return
    
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    
    content = content.replace('Color(0xFF161618)', 'MaterialTheme.colorScheme.surface')
    content = content.replace('Color(0xFF0A0A0C)', 'MaterialTheme.colorScheme.background')
    content = content.replace('Color(0xFF4A1010)', 'MaterialTheme.colorScheme.primaryContainer')
    content = content.replace('Color(0xFF2A1010)', 'MaterialTheme.colorScheme.secondaryContainer')
    content = content.replace('Color(0xFFA51B1B)', 'MaterialTheme.colorScheme.primary')
    content = content.replace('Color(0xFF2B2B2B)', 'MaterialTheme.colorScheme.surfaceVariant')
    content = content.replace('Color(0xFF3F3F3F)', 'MaterialTheme.colorScheme.surface')
    
    # Import MaterialTheme if missing and changes were made
    if original != content:
        if 'import androidx.compose.material3.MaterialTheme' not in content and 'import androidx.compose.material3.*' not in content:
            content = re.sub(r'(import [^\n]+)', r'\1\nimport androidx.compose.material3.MaterialTheme', content, count=1)
        with open(filepath, 'w') as f:
            f.write(content)

for root, dirs, files in os.walk('app/src/main/java/com/example/ui'):
    for file in files:
        if file.endswith('.kt'):
            process_file(os.path.join(root, file))

