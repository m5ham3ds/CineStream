import re

with open("app/src/main/java/com/example/ui/components/SharedUI.kt", "r") as f:
    content = f.read()

section_title_old = """@Composable
fun SectionTitleShared(title: String) {
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
        Text(
            text = "See All",
            style = MaterialTheme.typography.labelLarge,
            color = Color(0xFFE50914),
            modifier = Modifier.clickable { /* See all */ }
        )
    }
}"""

section_title_new = """@Composable
fun SectionTitleShared(title: String, onSeeAllClick: (() -> Unit)? = null) {
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
}"""

content = content.replace(section_title_old, section_title_new)

# The user mentioned fixing the sizes of the elements in the section above the categories.
# If they mean the Hero section in Home, wait, in Home it's HeroCarousel which is in HomeScreen.kt.
# Let's check HomeScreen.kt.

with open("app/src/main/java/com/example/ui/components/SharedUI.kt", "w") as f:
    f.write(content)
