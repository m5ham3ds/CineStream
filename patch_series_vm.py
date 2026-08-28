import re

with open("app/src/main/java/com/example/ui/screens/details/SeriesDetailsViewModel.kt", "r") as f:
    content = f.read()

imports = """import com.example.domain.models.Episode
import com.example.domain.models.Season"""
content = content.replace("import com.example.domain.models.Series", imports + "\nimport com.example.domain.models.Series")

ui_state_old = """data class SeriesDetailsUiState(
    val isLoading: Boolean = false,
    val series: Series? = null,
    val error: String? = null
)"""

ui_state_new = """data class SeriesDetailsUiState(
    val isLoading: Boolean = false,
    val series: Series? = null,
    val error: String? = null,
    val selectedSeason: Season? = null,
    val episodes: List<Episode> = emptyList(),
    val isEpisodesLoading: Boolean = false
)"""
content = content.replace(ui_state_old, ui_state_new)

load_series_old = """                if (series != null) {
                    _uiState.update { it.copy(series = series, isLoading = false) }
                } else {"""

load_series_new = """                if (series != null) {
                    val initialSeason = series.seasons.firstOrNull { it.seasonNumber > 0 } ?: series.seasons.firstOrNull()
                    _uiState.update { it.copy(series = series, isLoading = false, selectedSeason = initialSeason) }
                    initialSeason?.let { loadEpisodes(series.id, it.seasonNumber) }
                } else {"""
content = content.replace(load_series_old, load_series_new)

load_episodes = """
    fun selectSeason(season: Season) {
        val currentSeries = _uiState.value.series ?: return
        _uiState.update { it.copy(selectedSeason = season) }
        loadEpisodes(currentSeries.id, season.seasonNumber)
    }

    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            _uiState.update { it.copy(isEpisodesLoading = true) }
            try {
                val episodes = repository.getSeasonEpisodes(seriesId, seasonNumber)
                _uiState.update { it.copy(episodes = episodes, isEpisodesLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isEpisodesLoading = false) }
            }
        }
    }
}"""
content = content.replace("}\n}", "}\n" + load_episodes)

with open("app/src/main/java/com/example/ui/screens/details/SeriesDetailsViewModel.kt", "w") as f:
    f.write(content)
