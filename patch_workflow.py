import re

filepath = '.github/workflows/build.yml'
with open(filepath, 'r') as f:
    content = f.read()

# Remove the Generate debug keystore step
content = re.sub(
    r"      - name: Generate debug keystore\n        run: \|\n          keytool -genkey -v -keystore debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname \"C=US, O=Android, CN=Android Debug\"\n",
    "",
    content
)

with open(filepath, 'w') as f:
    f.write(content)
