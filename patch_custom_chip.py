import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    content = f.read()

old_chip_def = """@Composable
fun FilterChip(text: String, selected: Boolean) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .background(if (selected) Color(0xFFE50914) else Color(0xFF2C2C2E))
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable { /* TODO */ }
    ) {
        Text(text, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Medium)
    }
}"""

new_chip_def = """@Composable
fun CustomFilterChip(text: String, selected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .clickable { onClick() }
            .background(if (selected) Color(0xFFE50914) else Color(0xFF2C2C2E))
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Text(text, color = if (selected) Color.White else Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.Medium)
    }
}"""

content = content.replace(old_chip_def, new_chip_def)

# Also fix the usage in the items(categories) block that I just added
old_usage = """                            items(categories) { category ->
                                FilterChip(
                                    selected = selectedCategory == category,
                                    onClick = { selectedCategory = category },
                                    label = { Text(category, color = if (selectedCategory == category) Color.White else Color.Gray) },
                                    colors = FilterChipDefaults.filterChipColors(
                                        selectedContainerColor = primaryRed.copy(alpha = 0.2f),
                                        selectedLabelColor = Color.White
                                    )
                                )
                            }"""

new_usage = """                            items(categories) { category ->
                                CustomFilterChip(
                                    text = category,
                                    selected = selectedCategory == category,
                                    onClick = { selectedCategory = category }
                                )
                            }"""

content = content.replace(old_usage, new_usage)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(content)

