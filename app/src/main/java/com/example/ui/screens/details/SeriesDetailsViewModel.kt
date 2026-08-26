package com.example.ui.screens.details

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class SeriesDetailsUiState(
    val isLoading: Boolean = false,
    val series: Series? = null,
    val error: String? = null
)

class SeriesDetailsViewModel(
    private val repository: MediaRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(SeriesDetailsUiState())
    val uiState: StateFlow<SeriesDetailsUiState> = _uiState.asStateFlow()

    fun loadSeries(seriesId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val series = repository.getSeriesById(seriesId)
                if (series != null) {
                    _uiState.update { it.copy(series = series, isLoading = false) }
                } else {
                    _uiState.update { it.copy(error = "Series not found", isLoading = false) }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}
