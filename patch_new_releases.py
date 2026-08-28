import re

with open("app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt", "r") as f:
    content = f.read()

# Add Tabs
if "var selectedTab" not in content:
    content = content.replace("val uiState by viewModel.uiState.collectAsState()", "val uiState by viewModel.uiState.collectAsState()\n    var selectedTab by remember { mutableStateOf(\"All\") }")

tabs_ui = """
        Spacer(modifier = Modifier.height(16.dp))
        
        // Tabs
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .height(40.dp)
                .clip(RoundedCornerShape(8.dp))
                .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(8.dp)),
        ) {
            listOf("All", "Movies", "Series", "Anime").forEach { tab ->
                val isSelected = selectedTab == tab
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .background(if (isSelected) Color(0xFF2A2A2E).copy(alpha = 0.3f) else Color.Transparent)
                        .border(
                            width = 1.dp,
                            color = if (isSelected) Color(0xFFE50914) else Color.Transparent,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .clickable { selectedTab = tab },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tab,
                        color = if (isSelected) Color.White else Color.Gray,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        fontSize = 12.sp
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))

        val items = when (selectedTab) {
            "Movies" -> uiState.newReleasesMovies
            "Series" -> uiState.newReleasesSeries
            "Anime" -> uiState.animeSeries
            else -> (uiState.newReleasesMovies + uiState.newReleasesSeries + uiState.animeSeries).shuffled()
        }
"""

content = re.sub(r'Spacer\(modifier = Modifier\.height\(16\.dp\)\)\n\s*val items = \(uiState\.trendingMovies \+ uiState\.trendingSeries\)\.shuffled\(\)', tabs_ui.strip(), content)

# Check if border is imported
if "import androidx.compose.foundation.border" not in content:
    content = content.replace("import androidx.compose.foundation.background", "import androidx.compose.foundation.background\nimport androidx.compose.foundation.border\nimport androidx.compose.foundation.clickable")

with open("app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt", "w") as f:
    f.write(content)
