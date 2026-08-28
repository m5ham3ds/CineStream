import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

def replace_drawer(match):
    screen = match.group(1)
    return f"""DrawerItem(
                                icon = Icons.Default.Home,
                                label = "{screen}",
                                isSelected = currentRoute == Screen.{screen}.route,
                                onClick = {{
                                    if (currentRoute == Screen.{screen}.route) {{
                                        navController.popBackStack(Screen.{screen}.route, inclusive = true)
                                        navController.navigate(Screen.{screen}.route)
                                    }} else {{
                                        navController.navigate(Screen.{screen}.route)
                                    }}
                                    scope.launch {{ drawerState.close() }}
                                }}
                            )"""

content = re.sub(
    r'DrawerItem\(\s*icon = .*?,\s*label = "([^"]+)",\s*isSelected = currentRoute == Screen\.\1\.route,\s*onClick = \{\s*navController\.navigate\(Screen\.\1\.route\)\s*scope\.launch \{ drawerState\.close\(\) \}\s*\}\s*\)',
    replace_drawer,
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

