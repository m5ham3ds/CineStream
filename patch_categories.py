import os
import glob

def patch_file(filepath, main_category):
    with open(filepath, "r") as f:
        content = f.read()

    # 1. Patch the click logic
    old_click = ".clickable { selectedCategory = category"
    if old_click in content:
        new_click = f".clickable {{\n                            if (selectedCategory == category) {{\n                                selectedCategory = \"{main_category}\"\n                            }} else {{\n                                selectedCategory = category\n                            }}\n                        }}"
        # We need to be careful if it's category or category.name
        content = content.replace(".clickable { selectedCategory = category }", new_click)
        content = content.replace(".clickable { selectedCategory = category.name }", 
            f".clickable {{\n                            if (selectedCategory == category.name) {{\n                                selectedCategory = \"{main_category}\"\n                            }} else {{\n                                selectedCategory = category.name\n                            }}\n                        }}")

    with open(filepath, "w") as f:
        f.write(content)

patch_file("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "Home")
patch_file("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "Movies")
patch_file("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "Series")
patch_file("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "Anime")
