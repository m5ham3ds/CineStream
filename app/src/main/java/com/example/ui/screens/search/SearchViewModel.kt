package com.example.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class SearchUiState(
    val query: String = "",
    val isSearching: Boolean = false,
    val movieResults: List<Movie> = emptyList(),
    val seriesResults: List<Series> = emptyList()
)

@OptIn(FlowPreview::class)
class SearchViewModel(private val repository: MediaRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    private val queryFlow = MutableStateFlow("")

    init {
        viewModelScope.launch {
            queryFlow
                .debounce(500)
                .collect { q ->
                    if (q.isBlank()) {
                        _uiState.update { it.copy(movieResults = emptyList(), seriesResults = emptyList(), isSearching = false) }
                    } else {
                        performSearch(q)
                    }
                }
        }
    }

    fun onQueryChange(query: String) {
        _uiState.update { it.copy(query = query, isSearching = true) }
        queryFlow.value = query
    }

    private fun performSearch(query: String) {
        viewModelScope.launch {
            repository.getMovies().combine(repository.getSeries()) { movies, series ->
                val m = movies.filter { it.title.contains(query, ignoreCase = true) }
                val s = series.filter { it.title.contains(query, ignoreCase = true) }
                Pair(m, s)
            }.collect { (m, s) ->
                _uiState.update { it.copy(movieResults = m, seriesResults = s, isSearching = false) }
            }
        }
    }
}
