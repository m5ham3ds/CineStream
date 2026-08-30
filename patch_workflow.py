import re

filepath = '.github/workflows/build.yml'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """      - name: Setup Keystore
        run: |
          if [ -f "debug.keystore.base64" ]; then
            base64 -d debug.keystore.base64 > debug.keystore
          else
            echo "debug.keystore.base64 not found!"
            exit 1
          fi
      - name: Build Debug APK"""

content = content.replace("      - name: Build Debug APK", replacement)

with open(filepath, 'w') as f:
    f.write(content)
