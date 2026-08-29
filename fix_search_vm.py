import re

filepath = 'app/src/main/java/com/example/ui/screens/search/SearchViewModel.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Add import for ProviderManager
if 'import com.example.domain.providers.ProviderManager' not in content:
    content = content.replace('import androidx.lifecycle.viewModelScope', 'import androidx.lifecycle.viewModelScope\nimport com.example.domain.providers.ProviderManager')

search_impl = """
    private fun performSearch(query: String) {
        viewModelScope.launch {
            // Fetch TMDB results
            val (tmdbMovies, tmdbSeries) = repository.searchMulti(query)
            
            // Fetch Provider results
            val providerSeries = ProviderManager.searchProviders(query)
            
            // Deduplicate: If TMDB already has this title, exclude from provider results
            val tmdbTitles = (tmdbMovies.map { it.title.lowercase() } + tmdbSeries.map { it.title.lowercase() }).toSet()
            
            // Deduplicate within providers as well
            val uniqueProviderSeries = mutableListOf<Series>()
            val seenProviderTitles = mutableSetOf<String>()
            
            for (ps in providerSeries) {
                val titleLow = ps.title.lowercase()
                if (!tmdbTitles.contains(titleLow) && !seenProviderTitles.contains(titleLow)) {
                    uniqueProviderSeries.add(ps)
                    seenProviderTitles.add(titleLow)
                }
            }
            
            // Merge TMDB series and the unique Provider series
            val finalSeries = tmdbSeries + uniqueProviderSeries
            
            _uiState.update { it.copy(movieResults = tmdbMovies, seriesResults = finalSeries, isSearching = false) }
        }
    }
"""

content = re.sub(r'private fun performSearch.*?\}\n    \}', search_impl.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)
