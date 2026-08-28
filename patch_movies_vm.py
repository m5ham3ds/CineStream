import re

with open("app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("private fun loadMovies()", "fun loadMovies()")

with open("app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "w") as f:
    f.write(content)
