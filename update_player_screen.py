import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Change signature
content = content.replace("fun PlayerScreen(videoUrl: String, onBack: () -> Unit) {", "fun PlayerScreen(videoUrl: String, title: String, onBack: () -> Unit) {")

# Change title rendering
content = content.replace('Text("Now Playing", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)', 'Text("Now Playing", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)\n                    Text(title, color = Color.Gray, fontSize = 14.sp)')
content = content.replace('Text("Episode 1", color = Color.Gray, fontSize = 14.sp)', '')

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
