import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

# Add onNavigateToAnime to HomeScreen arguments
content = content.replace(
    "onNavigateToUpcoming: () -> Unit = {},",
    "onNavigateToUpcoming: () -> Unit = {},\n    onNavigateToAnime: () -> Unit = {},"
)

# Update Anime SectionTitle
content = content.replace(
    """SectionTitle("Anime", onSeeAllClick = {})""",
    """SectionTitle("Anime", onSeeAllClick = onNavigateToAnime)"""
)

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
