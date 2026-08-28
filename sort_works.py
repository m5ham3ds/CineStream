with open("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Text(\"Movies\"", "Text(\"Top Movies\"")
content = content.replace("Text(\"TV Shows\"", "Text(\"Top TV Shows\"")

with open("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "w") as f:
    f.write(content)
