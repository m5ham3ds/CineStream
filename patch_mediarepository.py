import re

with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "r") as f:
    content = f.read()

content = content.replace(
    "suspend fun getSeriesById(id: String): Series?",
    "suspend fun getSeriesById(id: String): Series?\n    suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>>"
)

with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "w") as f:
    f.write(content)
