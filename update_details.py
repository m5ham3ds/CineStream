import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Update MovieDetailsScreen signature
content = content.replace(
    "fun MovieDetailsScreen(",
    "fun MovieDetailsScreen(\n    onPersonClick: (String) -> Unit = {},"
)
content = content.replace(
    "fun SeriesDetailsScreen(",
    "fun SeriesDetailsScreen(\n    onPersonClick: (String) -> Unit = {},"
)

# Update CastMemberCard signature
content = content.replace(
    "fun CastMemberCard(cast: CastMember) {",
    "fun CastMemberCard(cast: CastMember, onClick: () -> Unit) {"
)
# Make CastMemberCard clickable
content = content.replace(
    "Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(80.dp)) {",
    "Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(80.dp).clickable { onClick() }) {"
)

# Update usage in MovieDetailsScreen and SeriesDetailsScreen
content = content.replace(
    "items(movie.cast) { CastMemberCard(it) }",
    "items(movie.cast) { CastMemberCard(it) { onPersonClick(it.id) } }"
)
content = content.replace(
    "items(series.cast) { CastMemberCard(it) }",
    "items(series.cast) { CastMemberCard(it) { onPersonClick(it.id) } }"
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
