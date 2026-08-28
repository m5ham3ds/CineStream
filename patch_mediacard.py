import re

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "r") as f:
    content = f.read()

imports = """
import kotlinx.coroutines.launch
import com.example.data.model.LibraryItem
"""

if "kotlinx.coroutines.launch" not in content:
    content = content.replace("import androidx.compose.runtime.Composable", imports + "\nimport androidx.compose.runtime.Composable")

# Replace the confirmButton logic
old_confirm = r'TextButton\(onClick = \{\s*isBookmarked = false\s*showRemoveDialog = false\s*\}\)'
new_confirm = """val scope = rememberCoroutineScope()
                TextButton(onClick = {
                    if (mediaId != null) {
                        scope.launch {
                            libraryRepository.removeFromLibrary(LibraryItem(mediaId, title, posterUrl, isMovie))
                        }
                    }
                    showRemoveDialog = false
                })"""

content = re.sub(old_confirm, new_confirm, content)

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "w") as f:
    f.write(content)

