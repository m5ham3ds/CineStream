import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("withTimeout(5000)", "withTimeout(15000)")
content = content.replace("withTimeout(10000)", "withTimeout(15000)")

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace("withTimeout(5000)", "withTimeout(15000)")
content2 = content2.replace("withTimeout(10000)", "withTimeout(15000)")

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content2)
