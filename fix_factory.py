with open("app/src/main/java/com/example/ui/ViewModelFactory.kt", "r") as f:
    content = f.read()

new_vm = """        if (modelClass.isAssignableFrom(com.example.ui.screens.details.PersonDetailsViewModel::class.java)) {
            return com.example.ui.screens.details.PersonDetailsViewModel(AppContainer.mediaRepository) as T
        }
        throw IllegalArgumentException"""

content = content.replace("        throw IllegalArgumentException", new_vm)

with open("app/src/main/java/com/example/ui/ViewModelFactory.kt", "w") as f:
    f.write(content)
