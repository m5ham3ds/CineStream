import re

with open("app/src/main/java/com/example/di/AppContainer.kt", "r") as f:
    content = f.read()

content = content.replace("MockMediaRepositoryImpl", "TmdbMediaRepositoryImpl")

with open("app/src/main/java/com/example/di/AppContainer.kt", "w") as f:
    f.write(content)

