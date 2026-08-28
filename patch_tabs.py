import re

# PopularScreen
with open("app/src/main/java/com/example/ui/screens/home/PopularScreen.kt", "r") as f:
    content = f.read()

content = content.replace('listOf("All", "Movies", "Series")', 'listOf("All", "Movies", "Series", "Anime")')
items_logic = """
        val items = when (selectedTab) {
            "Movies" -> uiState.trendingMovies
            "Series" -> uiState.trendingSeries
            "Anime" -> uiState.animeSeries
            else -> (uiState.trendingMovies + uiState.trendingSeries + uiState.animeSeries).shuffled()
        }
"""
content = re.sub(r'val items = when \(selectedTab\) \{.*?\n        \}', items_logic.strip(), content, flags=re.DOTALL)
with open("app/src/main/java/com/example/ui/screens/home/PopularScreen.kt", "w") as f:
    f.write(content)

# TrendingScreen
with open("app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt", "r") as f:
    content = f.read()

content = content.replace('listOf("All", "Movies", "Series")', 'listOf("All", "Movies", "Series", "Anime")')
items_logic_trending = """
        val items = when (selectedTab) {
            "Movies" -> uiState.trendingMovies
            "Series" -> uiState.trendingSeries
            "Anime" -> uiState.animeSeries
            else -> (uiState.trendingMovies + uiState.trendingSeries + uiState.animeSeries).shuffled()
        }
"""
content = re.sub(r'val items = when \(selectedTab\) \{.*?\n        \}', items_logic_trending.strip(), content, flags=re.DOTALL)
with open("app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt", "w") as f:
    f.write(content)

