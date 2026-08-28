import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Replace the search icon clickable
content = re.sub(
    r'Icon\(Icons.Default.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size\(24.dp\).clickable \{ isSearchExpanded = !isSearchExpanded \}\)',
    'Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size(24.dp).clickable { navController.navigate(Screen.Search.route) { launchSingleTop = true; restoreState = true } })',
    content
)

# Remove the AnimatedVisibility block
pattern = r'androidx.compose.animation.AnimatedVisibility\(visible = isSearchExpanded\) \{.*?(?=                        \} // end AnimatedVisibility|\Z).*?\}'
# Actually, since it spans many lines, let's use string operations instead.
