import re

with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

search_mock = """    override suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>> {
        return Pair(emptyList(), emptyList())
    }
"""

content = content.replace("}", search_mock + "\n}")

with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
