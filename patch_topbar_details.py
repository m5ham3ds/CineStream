import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

movie_scaffold_old = """
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("") },
                navigationIcon = {
                    IconButton(onClick = onBack, modifier = Modifier.background(Color.Black.copy(alpha=0.3f), CircleShape)) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = Color.Black
    ) { padding ->
"""

movie_scaffold_new = """
    Scaffold(
        containerColor = Color.Black
    ) { padding ->
"""

content = content.replace(movie_scaffold_old.strip(), movie_scaffold_new.strip())

series_scaffold_old = """
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("") },
                navigationIcon = {
                    IconButton(onClick = onBack, modifier = Modifier.background(Color.Black.copy(alpha=0.3f), CircleShape)) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = Color.Black
    ) { padding ->
"""
content = content.replace(series_scaffold_old.strip(), movie_scaffold_new.strip())

back_button = """
                // Hero Image with Gradient
                Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {
"""
back_button_new = """
                // Hero Image with Gradient
                Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {
"""
# We'll just float the back button over the content
# Wait, actually let's just put the back button in the Box

content = content.replace(
    "Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {",
    "Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {"
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
