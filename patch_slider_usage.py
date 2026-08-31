import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

content = re.sub(
    r'VerticalSlider\(\s*value = brightness,\s*onValueChange = \{ brightness = it \},\s*icon = Icons.Default.BrightnessMedium\s*\)',
    'VerticalSlider(\n                            value = brightness,\n                            onValueChange = { brightness = it },\n                            topIcon = Icons.Default.BrightnessMedium,\n                            bottomIcon = Icons.Default.PictureInPictureAlt\n                        )',
    content
)

content = re.sub(
    r'VerticalSlider\(\s*value = volume,\s*onValueChange = \{ volume = it \},\s*icon = Icons.AutoMirrored.Filled.VolumeUp\s*\)',
    'VerticalSlider(\n                            value = volume,\n                            onValueChange = { volume = it },\n                            topIcon = Icons.AutoMirrored.Filled.VolumeUp,\n                            bottomIcon = Icons.Default.Fullscreen\n                        )',
    content
)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
