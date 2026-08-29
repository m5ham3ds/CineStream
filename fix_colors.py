import os
import re

skip_files = ['Theme.kt', 'Color.kt', 'HeroCarousel.kt', 'MediaCard.kt', 'SharedUI.kt', 'AuthScreen.kt', 'SplashScreen.kt']

def process_file(filepath):
    filename = os.path.basename(filepath)
    if filename in skip_files:
        return
    
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    
    content = content.replace('Color.Black', 'MaterialTheme.colorScheme.background')
    content = content.replace('Color(0xFF1E1E20)', 'MaterialTheme.colorScheme.surface')
    content = content.replace('Color(0xFF2A2A2E)', 'MaterialTheme.colorScheme.surfaceVariant')
    content = content.replace('Color(0xFF141414)', 'MaterialTheme.colorScheme.surface')
    
    # Be careful with Color.White and Color.Gray
    content = content.replace('Color.White', 'MaterialTheme.colorScheme.onBackground')
    content = content.replace('Color.LightGray', 'MaterialTheme.colorScheme.onSurfaceVariant')
    content = content.replace('Color.Gray', 'MaterialTheme.colorScheme.onSurfaceVariant')
    
    # Fix the ones that might have broken .copy(...)
    content = content.replace('MaterialTheme.colorScheme.background.copy', 'Color.Black.copy')
    content = content.replace('MaterialTheme.colorScheme.onBackground.copy', 'Color.White.copy')
    
    # Import MaterialTheme if missing and changes were made
    if original != content:
        if 'import androidx.compose.material3.MaterialTheme' not in content and 'import androidx.compose.material3.*' not in content:
            content = re.sub(r'(import [^\n]+)', r'\1\nimport androidx.compose.material3.MaterialTheme', content, count=1)
        with open(filepath, 'w') as f:
            f.write(content)

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            process_file(os.path.join(root, file))

