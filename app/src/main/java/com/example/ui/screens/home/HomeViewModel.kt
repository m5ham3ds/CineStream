package com.example.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class HomeUiState(
    val isLoading: Boolean = true,
    val trendingMovies: List<Movie> = emptyList(),
    val trendingSeries: List<Series> = emptyList(),
    val actionMovies: List<Movie> = emptyList(),
    val animeSeries: List<Series> = emptyList(),
    val upcomingMovies: List<Movie> = emptyList(),
    val newReleasesMovies: List<Movie> = emptyList(),
    val newReleasesSeries: List<Series> = emptyList(),
    val error: String? = null
)

class HomeViewModel(
    private val repository: MediaRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    fun loadData() {
        _uiState.update { it.copy(isLoading = true, error = null) }
        viewModelScope.launch {
            repository.getTrendingMovies()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = false) } }
                .collect { movies ->
                    _uiState.update { it.copy(trendingMovies = movies) }
                }
            repository.getAnimeSeries()
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
            repository.getTrendingSeries()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = false) } }
                .collect { series ->
                    _uiState.update { it.copy(trendingSeries = series) }
                }
            repository.getMovies()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = false) } }
                .collect { allMovies ->
                    _uiState.update { 
                        it.copy(
                            actionMovies = allMovies.filter { m -> m.genres.contains("Action") },
                            isLoading = false
                        )
                    }
                }
        }
    }
}
