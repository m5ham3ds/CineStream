import os
import glob

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

# Add imports for CategoryItem
if 'import androidx.compose.material.icons.filled.LocalMovies' not in content:
    content = content.replace("import androidx.compose.material.icons.filled.ArrowDropDown", "import androidx.compose.material.icons.filled.ArrowDropDown\nimport androidx.compose.material.icons.filled.Category\nimport androidx.compose.material.icons.filled.LocalMovies\nimport androidx.compose.material.icons.filled.NewReleases\nimport androidx.compose.material.icons.filled.Star\nimport androidx.compose.ui.graphics.vector.ImageVector")

category_data = """    data class CategoryItem(val name: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)
    val categories = listOf(
        CategoryItem("Series", Icons.Default.LocalMovies),
        CategoryItem("Genres", Icons.Default.Category),
        CategoryItem("New Releases", Icons.Default.NewReleases),
        CategoryItem("Top Rated", Icons.Default.Star)
    )"""

content = content.replace("""    data class CategoryItem(val name: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)\n    val categories = listOf("All", "Trending", "New Releases", "Top Rated", "Genres")""", category_data)
content = content.replace("""    var selectedCategory by remember { mutableStateOf("All") }""", """    var selectedCategory by remember { mutableStateOf("Series") }""")

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)
