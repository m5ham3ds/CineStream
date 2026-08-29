import re

files = [
    'app/src/main/res/values/strings.xml',
    'app/src/main/res/values-ar/strings.xml'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove the lines added
    content = re.sub(r'\s*<string name="movies">.*?</string>', '', content)
    content = re.sub(r'\s*<string name="series">.*?</string>', '', content)
    content = re.sub(r'\s*<string name="anime">.*?</string>', '', content)
    content = re.sub(r'\s*<string name="library">.*?</string>', '', content)
    
    # Check if 'profile' is duplicated? The error didn't say profile was duplicated.
    # But let's leave 'profile' there, or if we want to be safe, we can check if it exists in strings_drawer.xml
    with open(filepath, 'w') as f:
        f.write(content)
