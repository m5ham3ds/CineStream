with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "r") as f:
    content = f.read()

content = content.replace(
    """                        Icon(
                imageVector = Icons.Outlined.BookmarkBorder, 
                contentDescription = "Bookmark", 
                tint = Color.White,
                modifier = Modifier.size(20.dp)
            )""",
    """                        IconButton(
                            onClick = { isBookmarked = !isBookmarked },
                            modifier = Modifier.size(24.dp)
                        ) {
                            Icon(
                                imageVector = if (isBookmarked) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder, 
                                contentDescription = "Bookmark", 
                                tint = Color.White,
                                modifier = Modifier.size(20.dp)
                            )
                        }"""
)

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "w") as f:
    f.write(content)
