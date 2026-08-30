import re

filepath = 'app/src/main/java/com/example/ui/components/SourceSelectionSheet.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    'mediaId: String,\n    mediaTitle: String = "Unknown",\n    isMovie: Boolean,\n    onDismiss: () -> Unit,',
    'mediaId: String,\n    mediaTitle: String = "Unknown",\n    isMovie: Boolean,\n    episodeId: String? = null,\n    onDismiss: () -> Unit,'
)

content = content.replace(
    'sources = ProviderManager.extractVideoLinks(mediaId, isMovie, if (!isMovie) "1" else null)',
    'sources = ProviderManager.extractVideoLinks(mediaId, isMovie, episodeId)'
)

with open(filepath, 'w') as f:
    f.write(content)
