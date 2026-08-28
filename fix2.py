import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

bad_vars = """                    var showSourceSheet by remember { mutableStateOf(false) }
                    var isDownloadMode by remember { mutableStateOf(false) }
                    var showSourceSheet by remember { mutableStateOf(false) }
                    var isDownloadMode by remember { mutableStateOf(false) }"""

good_vars = """                    var showSourceSheet by remember { mutableStateOf(false) }
                    var isDownloadMode by remember { mutableStateOf(false) }"""

content = content.replace(bad_vars, good_vars)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
