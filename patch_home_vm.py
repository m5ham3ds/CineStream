import re

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("private fun loadData()", "fun loadData()")

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(content)

