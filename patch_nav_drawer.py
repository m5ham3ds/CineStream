import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

def replacer(match):
    prefix = match.group(1)
    route = match.group(2)
    suffix = match.group(3)
    
    new_click = f"""{{
                        scope.launch {{ drawerState.close() }}
                        if (currentRoute == {route}) {{
                            navController.popBackStack({route}, inclusive = true)
                            navController.navigate({route})
                        }} else {{
                            navController.navigate({route})
                        }}
                    }}"""
    return prefix + new_click + suffix

content = re.sub(
    r'(onClick = )\{\s*scope\.launch \{ drawerState\.close\(\) \}\s*navController\.navigate\((Screen\.[a-zA-Z]+\.route)\)\s*\}(,?\s*modifier = )',
    replacer,
    content,
    flags=re.DOTALL
)

# For the Home item which is different:
def home_replacer(match):
    prefix = match.group(1)
    return prefix + """{
                        scope.launch { drawerState.close() }
                        if (currentRoute == Screen.Home.route) {
                            navController.popBackStack(Screen.Home.route, inclusive = true)
                            navController.navigate(Screen.Home.route)
                        } else {
                            navController.navigate(Screen.Home.route)
                        }
                    }"""

content = re.sub(
    r'(onClick = )\{\s*scope\.launch \{ drawerState\.close\(\) \}\s*navController\.navigate\(Screen\.Home\.route\)\s*\}',
    home_replacer,
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
