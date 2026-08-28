import re

with open("app/src/main/java/com/example/ui/screens/search/SearchViewModel.kt", "r") as f:
    content = f.read()

old_search = """    private fun performSearch(query: String) {
        viewModelScope.launch {
            repository.getMovies().combine(repository.getSeries()) { movies, series ->
                val m = movies.filter { it.title.contains(query, ignoreCase = true) }
                val s = series.filter { it.title.contains(query, ignoreCase = true) }
                Pair(m, s)
            }.collect { (m, s) ->
                _uiState.update { it.copy(movieResults = m, seriesResults = s, isSearching = false) }
            }
        }
    }"""
    
new_search = """    private fun performSearch(query: String) {
        viewModelScope.launch {
            val (m, s) = repository.searchMulti(query)
            _uiState.update { it.copy(movieResults = m, seriesResults = s, isSearching = false) }
        }
    }"""

content = content.replace(old_search, new_search)

with open("app/src/main/java/com/example/ui/screens/search/SearchViewModel.kt", "w") as f:
    f.write(content)
