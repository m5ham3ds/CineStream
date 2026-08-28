with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import re

# replace search icon
content = content.replace(
    """Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size(24.dp).clickable { isSearchExpanded = !isSearchExpanded })""",
    """Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.White, modifier = Modifier.size(24.dp).clickable { navController.navigate(Screen.Search.route) { launchSingleTop = true; restoreState = true } })"""
)

# remove AnimatedVisibility
start_idx = content.find("androidx.compose.animation.AnimatedVisibility(visible = isSearchExpanded)")
if start_idx != -1:
    end_idx = content.find("                    }", start_idx) 
    # we need to find the matching closing brace.
    brace_count = 0
    in_block = False
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
            in_block = True
        elif content[i] == '}':
            brace_count -= 1
        
        if in_block and brace_count == 0:
            end_idx = i + 1
            break
            
    content = content[:start_idx] + content[end_idx:]

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

