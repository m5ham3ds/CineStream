import re

with open("app/src/main/java/com/example/ui/ViewModelFactory.kt", "r") as f:
    content = f.read()

new_if = """        if (modelClass.isAssignableFrom(AnimeViewModel::class.java)) {
            return AnimeViewModel(AppContainer.mediaRepository) as T
        }
"""
content = content.replace("        throw IllegalArgumentException(\"Unknown ViewModel class\")", new_if + "        throw IllegalArgumentException(\"Unknown ViewModel class\")")

with open("app/src/main/java/com/example/ui/ViewModelFactory.kt", "w") as f:
    f.write(content)

