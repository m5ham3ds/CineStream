import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    content = f.read()

old_chips = """                            item { FilterChip(text = "All Messages", selected = true) }
                            item { FilterChip(text = "Groups", selected = false) }"""

new_chips = """                            item { FilterChip(text = "All Messages", selected = true) }
                            item { FilterChip(text = "Unread", selected = false) }
                            item { FilterChip(text = "Groups", selected = false) }
                            item { FilterChip(text = "Requests", selected = false) }"""

content = content.replace(old_chips, new_chips)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(content)

