with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "r") as f:
    content = f.read()

# count braces and fix it to the exact number
brace_count = 0
for char in content:
    if char == '{': brace_count += 1
    if char == '}': brace_count -= 1

if brace_count < 0:
    for _ in range(-brace_count):
        content = content.rstrip()
        if content.endswith('}'):
            content = content[:-1]
elif brace_count > 0:
    content += "}\n" * brace_count

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "w") as f:
    f.write(content)
