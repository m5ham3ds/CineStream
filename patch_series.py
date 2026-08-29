with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

import_statement = "import androidx.compose.material.icons.filled.*\n"
if import_statement not in content:
    content = content.replace("import androidx.compose.material.icons.filled.ArrowDropDown", "import androidx.compose.material.icons.filled.ArrowDropDown\nimport androidx.compose.material.icons.filled.Category\nimport androidx.compose.material.icons.filled.LocalMovies\nimport androidx.compose.material.icons.filled.NewReleases\nimport androidx.compose.material.icons.filled.Star\nimport androidx.compose.ui.graphics.vector.ImageVector")

category_data = """    data class CategoryItem(val name: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)
    val categories = listOf(
        CategoryItem("Series", Icons.Default.LocalMovies),
        CategoryItem("Genres", Icons.Default.Category),
        CategoryItem("New Releases", Icons.Default.NewReleases),
        CategoryItem("Top Rated", Icons.Default.Star)
    )"""

content = content.replace("var selectedCategory by remember { mutableStateOf(\"All\") }\n    val categories = listOf(\"All\", \"Trending\", \"New Releases\", \"Top Rated\", \"Genres\")",
    "var selectedCategory by remember { mutableStateOf(\"Series\") }\n" + category_data)

content = content.replace("items(categories) { category ->", "items(categories) { category ->")
# Wait, replacing the rendering logic of items(categories) is tricky.
# Let's just find and replace the whole LazyRow for categories.
