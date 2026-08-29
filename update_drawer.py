import re

filepath = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(filepath, 'r') as f:
    content = f.read()

drawer_additions = """
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                    label = { Text("Community", color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Social.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (currentRoute != Screen.Social.route) {
                            navController.navigate(Screen.Social.route)
                        }
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Download, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                    label = { Text("Offline Share", color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Share.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (currentRoute != Screen.Share.route) {
                            navController.navigate(Screen.Share.route)
                        }
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
"""

content = content.replace(
    'HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))',
    drawer_additions + '\n                                HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))',
    1
)

with open(filepath, 'w') as f:
    f.write(content)

