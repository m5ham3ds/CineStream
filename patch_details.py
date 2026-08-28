with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Replace TrailerCard intent behavior
content = content.replace(
    """val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://www.youtube.com/watch?v=${trailer.key}"))
                                context.startActivity(intent)""",
    """onPlay("trailer:${trailer.key}")"""
)

# And in MovieDetailsScreen/SeriesDetailsScreen navigation, we map "trailer:" to navigate to trailer route
# Oh wait, we passed `onPlay("trailer:...")`, let's handle that in AppNavigation!

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
