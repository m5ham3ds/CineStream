import re

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    content = f.read()

new_state = """    val animeSeries: List<Series> = emptyList(),
    val upcomingMovies: List<Movie> = emptyList(),
    val newReleasesMovies: List<Movie> = emptyList(),
    val newReleasesSeries: List<Series> = emptyList(),"""

content = content.replace("    val actionMovies: List<Movie> = emptyList(),", "    val actionMovies: List<Movie> = emptyList(),\n" + new_state)

loads = """            repository.getAnimeSeries()
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { animes ->
                    _uiState.update { it.copy(animeSeries = animes) }
                }
            repository.getUpcomingMovies()
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { upcoming ->
                    _uiState.update { it.copy(upcomingMovies = upcoming) }
                }
            repository.getNewReleasesMovies()
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { movies ->
                    _uiState.update { it.copy(newReleasesMovies = movies) }
                }
            repository.getNewReleasesSeries()
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { series ->
                    _uiState.update { it.copy(newReleasesSeries = series) }
                }
"""

content = content.replace("            repository.getTrendingSeries()", loads + "            repository.getTrendingSeries()")

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(content)
