import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# For movie:
movie_insert_point = "                SourceSelectionSheet("
movie_back_btn = """
            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = padding.calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(Color.Black.copy(alpha=0.3f), CircleShape)
            ) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
            }
"""
content = re.sub(
    r'(                SourceSelectionSheet\(\n                    mediaId = movie\.id,[\s\S]*?onDismiss = \{ showSourceSheet = false \},[\s\S]*?onSourceSelected = \{ source ->[\s\S]*?\}[\s\S]*?\)\n            \})',
    r'\1' + '\n' + movie_back_btn,
    content
)

content = re.sub(
    r'(                SourceSelectionSheet\(\n                    mediaId = series\.id,[\s\S]*?onDismiss = \{ showSourceSheet = false \},[\s\S]*?onSourceSelected = \{ source ->[\s\S]*?\}[\s\S]*?\)\n            \})',
    r'\1' + '\n' + movie_back_btn,
    content
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
