import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# I will add Suppress just to be absolutely sure.
content = content.replace("fun PlayerScreen(", "@Suppress(\"OPT_IN_USAGE\")\nfun PlayerScreen(")

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
