import re

filepath = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """            ModalDrawerSheet(
                drawerContainerColor = MaterialTheme.colorScheme.surface,
                modifier = Modifier.width(300.dp)
            ) {
                // Top Header Section with Gradient
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .background(
                            brush = Brush.verticalGradient(
                                colors = listOf(MaterialTheme.colorScheme.surfaceVariant, MaterialTheme.colorScheme.surface)
                            )
                        )
                        .padding(16.dp)
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.Top
                    ) {
                        Text(
                            text = "CineStream",
                            style = MaterialTheme.typography.headlineMedium.copy(
                                fontWeight = FontWeight.Bold,
                                fontFamily = FontFamily.Serif
                            ),
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.fillMaxWidth(),
                            textAlign = TextAlign.Start
                        )
                        Spacer(modifier = Modifier.weight(1f))
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.clickable {
                                scope.launch { drawerState.close() }
                                if (isGuest) {
                                    navController.navigate(Screen.Auth.route)
                                } else {
                                    navController.navigate(Screen.Profile.route)
                                }
                            }
                        ) {
                            Column {
                                Text(
                                    text = if (isGuest) "Guest User" else "E. Laurent",
                                    fontSize = 24.sp,
                                    fontFamily = FontFamily.SansSerif,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    if (!isGuest) {
                                        Icon(painter = painterResource(android.R.drawable.ic_dialog_info), contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(4.dp))
                                    }
                                    Text(
                                        text = if (isGuest) "Free Account" else "Premium User",
                                        fontSize = 14.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.weight(1f))
                            Box(
                                modifier = Modifier
                                    .size(70.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onSurfaceVariant)
                                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(40.dp))
                            }
                        }
                    }
                }
                
                Column(modifier = Modifier.weight(1f).verticalScroll(androidx.compose.foundation.rememberScrollState())) {
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Home, contentDescription = null, tint = if (currentRoute == Screen.Home.route) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onBackground) },
                        label = { Text(stringResource(R.string.home), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Home.route,
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            unselectedContainerColor = Color.Transparent
                        ),
                        shape = RoundedCornerShape(16.dp),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.Home.route) {
                                navController.popBackStack(Screen.Home.route, inclusive = true)
                                navController.navigate(Screen.Home.route)
                            } else {
                                navController.navigate(Screen.Home.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Favorite, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.library), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Library.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.Library.route) {
                                navController.popBackStack(Screen.Library.route, inclusive = true)
                                navController.navigate(Screen.Library.route)
                            } else {
                                navController.navigate(Screen.Library.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Settings, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.settings), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Settings.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.Settings.route) {
                                navController.popBackStack(Screen.Settings.route, inclusive = true)
                                navController.navigate(Screen.Settings.route)
                            } else {
                                navController.navigate(Screen.Settings.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
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
                        label = { Text(stringResource(R.string.downloads), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Downloads.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.Downloads.route) {
                                navController.popBackStack(Screen.Downloads.route, inclusive = true)
                                navController.navigate(Screen.Downloads.route)
                            } else {
                                navController.navigate(Screen.Downloads.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Share, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
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

                    HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Info, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.about_app), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.About.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.About.route) {
                                navController.popBackStack(Screen.About.route, inclusive = true)
                                navController.navigate(Screen.About.route)
                            } else {
                                navController.navigate(Screen.About.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.AutoMirrored.Filled.Help, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.help_support), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = false,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = { scope.launch { drawerState.close() } },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                }
                
                HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))

                // Bottom Area (Logout)"""

# I need to find ModalDrawerSheet( ... ) { ... // Bottom Area (Logout)
pattern = r"ModalDrawerSheet\(\s*drawerContainerColor = MaterialTheme\.colorScheme\.surface,\s*modifier = Modifier\.width\(300\.dp\)\s*\)\s*\{(.*?)(?=// Bottom Area \(Logout\))"

content = re.sub(pattern, replacement.replace("ModalDrawerSheet(\n                drawerContainerColor = MaterialTheme.colorScheme.surface,\n                modifier = Modifier.width(300.dp)\n            ) {\n", "ModalDrawerSheet(\n                drawerContainerColor = MaterialTheme.colorScheme.surface,\n                modifier = Modifier.width(300.dp)\n            ) {\n") , content, flags=re.DOTALL)


with open(filepath, 'w') as f:
    f.write(content)
