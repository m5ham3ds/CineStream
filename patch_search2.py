import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

bad_else_if = """ else if (item.mediaType == "tv") {
                    series.add(Series(
                        id = item.id.toString(),
                        title = item.name ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        rating = item.voteAverage ?: 0.0,
                        releaseYear = item.firstAirDate?.take(4) ?: "Unknown",
                        genres = emptyList(),
                        seasons = 1
                    ))
                }"""
content = content.replace(bad_else_if, "")

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(content)
