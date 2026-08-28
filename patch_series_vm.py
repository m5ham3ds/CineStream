import re

with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("private fun loadSeries()", "fun loadSeries()")

with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "w") as f:
    f.write(content)
