import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# For MovieDetailsScreen
movie_pattern = r'(fun MovieDetailsScreen.*?)(            Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.verticalScroll\(rememberScrollState\(\)\)\n\s*\) \{)'
movie_repl = r'\1            val ptrState = rememberPullToRefreshState()\n            PullToRefreshBox(\n                isRefreshing = uiState.isLoading,\n                onRefresh = { viewModel.loadMovie(movieId) },\n                state = ptrState,\n                modifier = Modifier.fillMaxSize().padding(padding)\n            ) {\n\2'
content = re.sub(movie_pattern, movie_repl, content, flags=re.DOTALL | re.MULTILINE)

# For SeriesDetailsScreen
series_pattern = r'(fun SeriesDetailsScreen.*?)(            Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.verticalScroll\(rememberScrollState\(\)\)\n\s*\) \{)'
series_repl = r'\1            val ptrState = rememberPullToRefreshState()\n            PullToRefreshBox(\n                isRefreshing = uiState.isLoading,\n                onRefresh = { viewModel.loadSeries(seriesId) },\n                state = ptrState,\n                modifier = Modifier.fillMaxSize().padding(padding)\n            ) {\n\2'
content = re.sub(series_pattern, series_repl, content, flags=re.DOTALL | re.MULTILINE)

# Need to add `}` before `if (showSourceSheet)`
content = re.sub(
    r'(            if \(showSourceSheet\) \{)',
    r'            }\n\1',
    content
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "r") as f:
    content = f.read()

person_pattern = r'(fun PersonDetailsScreen.*?)(            Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.verticalScroll\(rememberScrollState\(\)\)\n\s*\) \{)'
person_repl = r'\1            val ptrState = rememberPullToRefreshState()\n            PullToRefreshBox(\n                isRefreshing = uiState.isLoading,\n                onRefresh = { viewModel.loadPerson(personId) },\n                state = ptrState,\n                modifier = Modifier.fillMaxSize().padding(padding)\n            ) {\n\2'
content = re.sub(person_pattern, person_repl, content, flags=re.DOTALL | re.MULTILINE)

# Need to add `}` before `if (selectedImage != null)`
content = re.sub(
    r'(            if \(selectedImage != null\) \{)',
    r'            }\n\1',
    content
)

with open("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "w") as f:
    f.write(content)

