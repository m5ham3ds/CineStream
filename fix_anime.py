import re

filepath = 'app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    'var selectedCategory by remember { mutableStateOf(stringResource(R.string.anime)) }',
    'val animeStr = stringResource(R.string.anime)\n    var selectedCategory by remember { mutableStateOf(animeStr) }'
)
content = content.replace(
    'CategoryItem(stringResource(R.string.anime), Icons.Default.LocalMovies)',
    'CategoryItem(animeStr, Icons.Default.LocalMovies)'
)
content = content.replace(
    'selectedCategory = stringResource(R.string.anime)',
    'selectedCategory = animeStr'
)
content = content.replace(
    'selectedCategory == stringResource(R.string.anime)',
    'selectedCategory == animeStr'
)

with open(filepath, 'w') as f:
    f.write(content)

