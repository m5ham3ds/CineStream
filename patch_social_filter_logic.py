import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    content = f.read()

# Add a selectedCategory state
state_code = """    val searchResults by viewModel.searchResults.collectAsState()
    var selectedCategory by remember { mutableStateOf("All Messages") }
"""
content = content.replace("    val searchResults by viewModel.searchResults.collectAsState()", state_code)

# Replace the chips block
old_chips = """                        LazyRow(
                            modifier = Modifier.padding(top = 16.dp, bottom = 8.dp),
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            item { FilterChip(text = "All Messages", selected = true) }
                            item { FilterChip(text = "Unread", selected = false) }
                            item { FilterChip(text = "Groups", selected = false) }
                            item { FilterChip(text = "Requests", selected = false) }
                        }"""

new_chips = """                        LazyRow(
                            modifier = Modifier.padding(top = 16.dp, bottom = 8.dp),
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            val categories = listOf("All Messages", "Unread", "Groups", "Requests")
                            items(categories) { category ->
                                FilterChip(
                                    selected = selectedCategory == category,
                                    onClick = { selectedCategory = category },
                                    label = { Text(category, color = if (selectedCategory == category) Color.White else Color.Gray) },
                                    colors = FilterChipDefaults.filterChipColors(
                                        selectedContainerColor = primaryRed.copy(alpha = 0.2f),
                                        selectedLabelColor = Color.White
                                    )
                                )
                            }
                        }"""

content = content.replace(old_chips, new_chips)

# Replace the items(conversations) to filter
old_items = """                        LazyColumn(
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(conversations) {"""

new_items = """                        LazyColumn(
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            val filteredConversations = when (selectedCategory) {
                                "Unread" -> conversations.filter { 
                                    val otherUserId = it.participants.firstOrNull { p -> p != currentUser?.uid } ?: ""
                                    (it.unreadCounts[otherUserId] ?: 0) > 0 
                                }
                                else -> conversations
                            }
                            items(filteredConversations) {"""
content = content.replace(old_items, new_items)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(content)

