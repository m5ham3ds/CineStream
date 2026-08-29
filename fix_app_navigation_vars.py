import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

old_updating = 'var isUpdatingData by remember { mutableStateOf(true) }'
new_updating = """var isUpdatingData by remember { mutableStateOf(true) }
    var updateFinishedShowGreen by remember { mutableStateOf(false) }
    
    androidx.compose.runtime.LaunchedEffect(updateFinishedShowGreen) {
        if (updateFinishedShowGreen) {
            kotlinx.coroutines.delay(2000)
            isUpdatingData = false
            updateFinishedShowGreen = false
        }
    }
    
    val primaryColor by userPrefs.primaryColor.collectAsState(initial = 0)
    val primaryColorVal = Color(if (primaryColor == 0) 0xFFE50914 else primaryColor.toLong())
"""
content = content.replace(old_updating, new_updating)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
