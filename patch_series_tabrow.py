with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

import re

# We need to replace the LazyRow for the tabs.
# It starts around: LazyRow( modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
# and ends before: SectionTitleShared("Trending Series", onSeeAllClick = onNavigateToTrending) or something similar.

# Let's just find "items(categories) { category ->" and replace it
# Wait, I already changed SeriesScreen to use `CategoryItem` data class?
# Ah, I replaced the data class definition, but NOT the rendering code.
# The rendering code in SeriesScreen uses `category` as a String (because it WAS a String).
# Now it is `category.name`.

replacement = """            items(categories) { category ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (selectedCategory == category.name) Color(0xFFE50914) else Color(0xFF1E1E20))
                        .clickable {
                            if (selectedCategory == category.name) {
                                selectedCategory = "Series"
                            } else {
                                selectedCategory = category.name
                            }
                        }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = category.icon, 
                            contentDescription = category.name, 
                            tint = if (selectedCategory == category.name) Color.White else Color.Gray,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = category.name,
                            color = if (selectedCategory == category.name) Color.White else Color.Gray,
                            fontSize = 14.sp,
                            fontWeight = if (selectedCategory == category.name) FontWeight.SemiBold else FontWeight.Normal
                        )
                    }
                }
            }"""

# Use regex to replace the `items(categories) { ... }` block
# From `items(categories) { category ->` to the matching `}` for items block.
# Actually, it's safer to just split and combine or replace the exact known string.

content = re.sub(r"items\(categories\) \{ category ->.*?\}\s*\}\s*\}", replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)
