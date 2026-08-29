import re

filepath = 'app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Update currentStartScreenName
old_current_start = """    val currentStartScreenName = when(startScreen) {
        "search" -> stringResource(R.string.search)
        "downloads" -> stringResource(R.string.downloads)
        "settings" -> stringResource(R.string.settings)
        else -> stringResource(R.string.home)
    }"""
new_current_start = """    val currentStartScreenName = when(startScreen) {
        "search" -> stringResource(R.string.search)
        "downloads" -> stringResource(R.string.downloads)
        "settings" -> stringResource(R.string.settings)
        "movies" -> stringResource(R.string.movies)
        "series" -> stringResource(R.string.series)
        "anime" -> stringResource(R.string.anime)
        "library" -> stringResource(R.string.library)
        "profile" -> stringResource(R.string.profile)
        else -> stringResource(R.string.home)
    }"""
content = content.replace(old_current_start, new_current_start)

# Update the BottomSheet items
old_list_items = """                ListItem(
                    headlineContent = { Text(stringResource(R.string.home)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("home"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.search)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("search"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.downloads)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("downloads"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.settings)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("settings"); showStartScreenSheet = false } }
                )"""

new_list_items = """                ListItem(
                    headlineContent = { Text(stringResource(R.string.home)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("home"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.movies)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("movies"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.series)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("series"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.anime)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("anime"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.search)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("search"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.library)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("library"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.downloads)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("downloads"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.profile)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("profile"); showStartScreenSheet = false } }
                )
                ListItem(
                    headlineContent = { Text(stringResource(R.string.settings)) },
                    modifier = Modifier.clickable { coroutineScope.launch { userPrefs.saveStartScreen("settings"); showStartScreenSheet = false } }
                )"""
content = content.replace(old_list_items, new_list_items)

with open(filepath, 'w') as f:
    f.write(content)
