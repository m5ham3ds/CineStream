import os

files = [
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt"
]

for f in files:
    with open(f, "r") as file:
        content = file.read()
    
    if "import androidx.compose.foundation.lazy.itemsIndexed" not in content:
        content = content.replace("import androidx.compose.foundation.lazy.items", "import androidx.compose.foundation.lazy.items\nimport androidx.compose.foundation.lazy.itemsIndexed")
        
    with open(f, "w") as file:
        file.write(content)
