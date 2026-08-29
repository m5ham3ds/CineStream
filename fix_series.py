import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

# Make sure CategoryItem exists
if "data class CategoryItem" not in content:
    content = content.replace("val categories = listOf", "data class CategoryItem(val name: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)\n    val categories = listOf")

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)
