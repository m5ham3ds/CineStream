import re

filepath = 'app/src/main/java/com/example/ui/components/BatchDownloadSheet.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    'title = "${series.title} - S${ep.seasonNumber}E${ep.episodeNumber}",',
    'title = "${series.title} - S${currentSeason?.seasonNumber}E${ep.episodeNumber}",'
)

with open(filepath, 'w') as f:
    f.write(content)


filepath = 'app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    'val isFavorite by libraryRepository.isLibraryItem(seriesId).collectAsState(initial = false)',
    'val isFavorite by libraryRepository.isItemInLibrary(seriesId).collectAsState(initial = false)'
)

content = content.replace(
    'Text(series.year, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)',
    'Text(series.year.toString(), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)'
)

content = content.replace(
    'libraryRepository.removeFromLibrary(seriesId)',
    'libraryRepository.removeFromLibrary(LibraryItem(id = series.id, title = series.title, posterUrl = series.posterUrl, isMovie = false))'
)

content = content.replace(
    'mediaTitle = "${series.title} S${selectedEpisodeForSource?.seasonNumber}E${selectedEpisodeForSource?.episodeNumber}",',
    'mediaTitle = "${series.title} S${uiState.selectedSeason?.seasonNumber}E${selectedEpisodeForSource?.episodeNumber}",'
)

content = content.replace(
    'title = "${series.title} - S${ep.seasonNumber}E${ep.episodeNumber}"',
    'title = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"'
)

# Insert the combinedClickable import at the top
import_str = 'import androidx.compose.foundation.combinedClickable'
if import_str not in content:
    content = content.replace('import androidx.compose.foundation.clickable', 'import androidx.compose.foundation.clickable\nimport androidx.compose.foundation.combinedClickable')

with open(filepath, 'w') as f:
    f.write(content)

