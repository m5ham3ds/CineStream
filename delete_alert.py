import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# find "var showEditProfile"
content = re.sub(r'var showEditProfile by remember.*?$', '', content, flags=re.MULTILINE)

# find the whole if (showEditProfile... AlertDialog block
# Since there might be nested braces, it's easier to just match the lines.

lines = content.split('\n')
new_lines = []
skip = False
brace_count = 0

for line in lines:
    if "if (showEditProfile && currentUser != null) {" in line:
        skip = True
        brace_count = 1
        continue
    
    if skip:
        if "{" in line:
            brace_count += line.count("{")
        if "}" in line:
            brace_count -= line.count("}")
        if brace_count == 0:
            skip = False
        continue
    
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write('\n'.join(new_lines))

