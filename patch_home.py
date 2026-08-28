import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

new_sections = """
        Spacer(modifier = Modifier.height(24.dp))
        
        // Anime
        if (uiState.animeSeries.isNotEmpty()) {
            SectionTitle("Anime", onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.animeSeries) { index, series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = 0,
                        rating = series.rating,
                        year = series.year,
                        isMovie = false,
                        onClick = { onSeriesClick(series.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = false
                            selectedMediaId = series.id
                            selectedMediaTitle = series.title
                            selectedMediaPoster = series.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // Coming Soon
        if (uiState.upcomingMovies.isNotEmpty()) {
            SectionTitle("Coming Soon", onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.upcomingMovies) { index, movie ->
                    MediaCard(
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        rank = 0,
                        rating = movie.rating,
                        year = movie.year,
                        onClick = { onMovieClick(movie.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = movie.id
                            selectedMediaTitle = movie.title
                            selectedMediaPoster = movie.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // New Releases
        if (uiState.newReleasesMovies.isNotEmpty()) {
            SectionTitle("New Releases", onSeeAllClick = onNavigateToNewReleases)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = (uiState.newReleasesMovies.take(10) + uiState.newReleasesSeries.map { 
                    Movie(it.id, it.title, it.overview, it.posterUrl, it.backdropUrl, it.rating, it.year, it.genres)
                }.take(10)).shuffled()
                itemsIndexed(mix) { index, item ->
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = 0,
                        rating = item.rating,
                        year = item.year,
                        onClick = { onMovieClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
"""

content = content.replace("    }\n        if (showBottomSheet) {", new_sections + "\n    }\n        if (showBottomSheet) {")

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
