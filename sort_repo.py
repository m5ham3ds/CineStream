with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

content = content.replace(
    """PersonDetails(
                id = response.id.toString(),""",
    """movies.sortByDescending { it.rating }
            series.sortByDescending { it.rating }

            PersonDetails(
                id = response.id.toString(),"""
)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
