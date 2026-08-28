with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace(
    "Icon(if (isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder, contentDescription = \"Favorite\", tint = if (isFavorite) Color.Red else Color.White)",
    "Icon(if (isFavorite) Icons.Default.Bookmark else Icons.Default.BookmarkBorder, contentDescription = \"Favorite\", tint = Color.White)"
)

# Need to import Bookmark and BookmarkBorder
if "Bookmark" not in content:
    content = content.replace(
        "import androidx.compose.material.icons.filled.Favorite",
        "import androidx.compose.material.icons.filled.Favorite\nimport androidx.compose.material.icons.filled.Bookmark\nimport androidx.compose.material.icons.filled.BookmarkBorder"
    )

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
