import re

filepath = 'app/src/main/java/com/example/ui/screens/social/SocialScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Remove topBar
top_bar_pattern = r"        topBar = \{\s*TopAppBar\(\s*title = \{ Text\(\"Community\", fontWeight = FontWeight\.Bold\) \},\s*navigationIcon = \{\s*IconButton\(onClick = onBack\) \{ Icon\(Icons\.AutoMirrored\.Filled\.ArrowBack, contentDescription = \"Back\"\) \}\s*\},\s*colors = TopAppBarDefaults\.topAppBarColors\(containerColor = MaterialTheme\.colorScheme\.background\)\s*\)\s*\},"
content = re.sub(top_bar_pattern, "", content, flags=re.DOTALL)


with open(filepath, 'w') as f:
    f.write(content)
