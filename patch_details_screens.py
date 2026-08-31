import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Replace signatures
content = content.replace("onPlay: (String) -> Unit,", "onPlay: (String, String) -> Unit,")
content = content.replace("onPlay: (String) -> Unit", "onPlay: (String, String) -> Unit")

# Replace Movie onPlay
content = content.replace('onPlay("local_offline_file://${downloadItem.id}")', 'onPlay(movie.title, "local_offline_file://${downloadItem.id}")')
content = content.replace('onPlay(source.url)', 'onPlay(movie.title, source.url)')

# Replace Series onPlay (trailers)
content = content.replace('onPlay("trailer:${trailer.key}")', 'onPlay(series.title, "trailer:${trailer.key}")')
# Replace Series onPlay (episodes)
content = content.replace('onPlay(source.url)', 'onPlay("${series.title} - ${ep.title}", source.url)')

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
