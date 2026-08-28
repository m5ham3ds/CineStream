import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add import for ExpandableSearchBar
if "import com.example.ui.components.ExpandableSearchBar" not in content:
    content = content.replace("import com.example.ui.components.BottomNavBar", "import com.example.ui.components.BottomNavBar\nimport com.example.ui.components.ExpandableSearchBar")

# We want to replace the Icon(Icons.Default.Search...) with our ExpandableSearchBar
# The search icon is around line 389. We need to find the `// Right Icons` block.
# We also have `var isSearchExpanded by remember { mutableStateOf(false) }` on line 91.

old_search = r'Icon\(Icons\.Default\.Search, contentDescription = "Search", tint = Color\.White, modifier = Modifier\.size\(24\.dp\)\.clickable \{ navController\.navigate\(Screen\.Search\.route\) \{ launchSingleTop = true; restoreState = true \} \}\)'
new_search = """
                            Box(modifier = Modifier.weight(2f), contentAlignment = Alignment.CenterEnd) {
                                ExpandableSearchBar(
                                    isExpanded = isSearchExpanded,
                                    onExpandedChange = { isSearchExpanded = it },
                                    onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                                    onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                                )
                            }
"""

content = re.sub(old_search, new_search, content)

# But we need to make sure the Space around it is responsive. If isSearchExpanded is true, we want to hide the App Name.
# Let's do a better replacement:

better_header = """
                            if (isSearchExpanded) {
                                ExpandableSearchBar(
                                    isExpanded = isSearchExpanded,
                                    onExpandedChange = { isSearchExpanded = it },
                                    onMovieClick = { id -> navController.navigate(Screen.MovieDetails.createRoute(id)) },
                                    onSeriesClick = { id -> navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                                )
                            } else {
                                // Right Icons
                                Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size(24.dp).clickable { isSearchExpanded = true })
                                Spacer(modifier = Modifier.width(16.dp))
                                BadgedBox(
                                    badge = {
                                        Badge(
                                            containerColor = Color(0xFFE50914), // Red badge
                                            contentColor = Color.White,
                                            modifier = Modifier.offset(x = (-4).dp, y = 4.dp)
                                        ) {
                                            Text("1")
                                        }
                                    }
                                ) {
                                    Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = Color.White, modifier = Modifier.size(24.dp))
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Icon(Icons.Default.Menu, contentDescription = "Menu", tint = Color.White, modifier = Modifier.size(24.dp).clickable { scope.launch { drawerState.open() } })
                            }
"""

# Find the block from `// Right Icons` down to `Icon(Icons.Default.Menu...)` and replace it.
block_to_replace = r'(?s)// Right Icons.*?Icon\(Icons\.Default\.Menu, contentDescription = "Menu", tint = Color\.White, modifier = Modifier\.size\(24\.dp\)\.clickable \{ scope\.launch \{ drawerState\.open\(\) \} \}\)'

content = re.sub(block_to_replace, better_header, content)

# Also hide "CineStream" text and Avatar when expanded
hide_center = r'(?s)(// Avatar on left.*?)(Spacer\(modifier = Modifier\.weight\(1f\)\)\s*// Center App Name\s*Text\(\s*"CineStream",.*?fontSize = 22\.sp\s*\)\s*Spacer\(modifier = Modifier\.weight\(1f\)\))'

def replacement(match):
    return match.group(1) + """
                            if (!isSearchExpanded) {
                                """ + match.group(2).replace('\n', '\n                                ') + """
                            } else {
                                Spacer(modifier = Modifier.width(16.dp))
                            }
    """

content = re.sub(hide_center, replacement, content)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

