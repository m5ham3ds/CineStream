import re

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

section_title_code = """
@Composable
fun SectionTitle(title: String, onSeeAllClick: (() -> Unit)? = null) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        if (onSeeAllClick != null) {
            Text(
                text = "See All",
                style = MaterialTheme.typography.labelLarge,
                color = Color(0xFFE50914),
                modifier = Modifier.clickable { onSeeAllClick() }
            )
        }
    }
}
"""

if "fun SectionTitle(" not in content:
    content += "\n" + section_title_code

with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
