import os
import re

files = [
    ("app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt", "Trending", "Now", "See what's popular today"),
    ("app/src/main/java/com/example/ui/screens/home/PopularScreen.kt", "Popular", "Picks", "Most watched this week"),
    ("app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt", "New", "Releases", "Latest additions"),
    ("app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt", "Coming", "Soon", "Upcoming movies & series")
]

for file_path, t1, t2, sub in files:
    with open(file_path, "r") as f:
        content = f.read()
    
    # ensure import exists
    if "import com.example.ui.components.CustomTopBar" not in content:
        content = content.replace("import com.example.ui.components.MediaCard", "import com.example.ui.components.MediaCard\nimport com.example.ui.components.CustomTopBar")
    
    # replace CenterAlignedTopAppBar
    regex = r"CenterAlignedTopAppBar\([\s\S]*?navigationIcon = \{[\s\S]*?\},[\s\S]*?colors = TopAppBarDefaults[\s\S]*?\)"
    # Note: trending doesn't have colors = TopAppBarDefaults
    # Wait, let's just use a more generic replace
    
    regex2 = r"CenterAlignedTopAppBar\([\s\S]*?\}\n            \)(,?)(\s*)"
    
    new_bar = f"""CustomTopBar(
            titleFirst = "{t1}",
            titleSecond = "{t2}",
            subtitle = "{sub}",
            onBack = onBack,
            showFilter = true
        )"""
    
    # For TrendingScreen
    content = re.sub(r'CenterAlignedTopAppBar\([\s\S]*?\}\n\s*\)', new_bar, content, count=1)
    
    with open(file_path, "w") as f:
        f.write(content)

