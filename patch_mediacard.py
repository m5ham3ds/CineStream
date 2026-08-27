import re

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "r") as f:
    content = f.read()

# Add imports for runtime state and dialog
imports = """import androidx.compose.runtime.*
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.TextButton
import androidx.compose.material3.IconButton
import androidx.compose.material.icons.filled.Bookmark
"""
content = content.replace("import androidx.compose.runtime.Composable", imports + "import androidx.compose.runtime.Composable")

# Update MediaCard signature and body
media_card_old = """fun MediaCard(
    title: String,
    posterUrl: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    onLongClick: (() -> Unit)? = null,
    rank: Int? = null,
    rating: Double = 8.7,
    year: String = "2024",
    isMovie: Boolean = true // Just to differentiate some icons if needed, but not right now
) {"""

media_card_new = """fun MediaCard(
    title: String,
    posterUrl: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    onLongClick: (() -> Unit)? = null,
    rank: Int? = null,
    rating: Double = 8.7,
    year: String = "2024",
    isMovie: Boolean = true
) {
    var isBookmarked by remember { mutableStateOf(false) }
    var showRemoveDialog by remember { mutableStateOf(false) }

    if (showRemoveDialog) {
        AlertDialog(
            onDismissRequest = { showRemoveDialog = false },
            title = { Text("إزالة من المفضلة", color = Color.White) },
            text = { Text("هل أنت متأكد أنك تريد إزالة هذا العمل من المفضلة؟", color = Color.LightGray) },
            confirmButton = {
                TextButton(onClick = {
                    isBookmarked = false
                    showRemoveDialog = false
                }) {
                    Text("إزالة", color = Color(0xFFE50914))
                }
            },
            dismissButton = {
                TextButton(onClick = { showRemoveDialog = false }) {
                    Text("إلغاء", color = Color.White)
                }
            },
            containerColor = Color(0xFF1E1E20)
        )
    }
"""

content = content.replace(media_card_old, media_card_new)

# Replace Bookmark icon part
bookmark_old = """                        Icon(
                imageVector = Icons.Outlined.BookmarkBorder, 
                 contentDescription = "Bookmark", 
                 tint = Color.White,
                modifier = Modifier.size(20.dp)
            )"""

bookmark_new = """                    IconButton(
                        onClick = { 
                            if (isBookmarked) showRemoveDialog = true else isBookmarked = true 
                        },
                        modifier = Modifier.size(24.dp)
                    ) {
                        Icon(
                            imageVector = if (isBookmarked) Icons.Default.Bookmark else Icons.Outlined.BookmarkBorder, 
                            contentDescription = "Bookmark", 
                            tint = if (isBookmarked) Color(0xFFE50914) else Color.White,
                            modifier = Modifier.size(20.dp)
                        )
                    }"""

content = content.replace(bookmark_old, bookmark_new)

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "w") as f:
    f.write(content)
