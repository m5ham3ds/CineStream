import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

new_drawer = """        drawerContent = {
            ModalDrawerSheet(
                drawerContainerColor = Color(0xFF161618),
                modifier = Modifier.width(300.dp)
            ) {
                // Top Header Section with Gradient
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .background(
                            brush = Brush.verticalGradient(
                                colors = listOf(Color(0xFF2B2B2B), Color(0xFF161618))
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
                            color = Color(0xFFE50914),
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
                                    color = Color.White
                                )
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    if (!isGuest) {
                                        Icon(painter = painterResource(android.R.drawable.ic_dialog_info), contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(4.dp))
                                    }
                                    Text(
                                        text = if (isGuest) "Free Account" else "Premium User",
                                        fontSize = 14.sp,
                                        color = Color.LightGray
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.weight(1f))
                            Box(
                                modifier = Modifier
                                    .size(70.dp)
                                    .clip(CircleShape)
                                    .background(Color.Gray)
                                    .border(2.dp, Color(0xFFE50914), CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Person, contentDescription = "Avatar", tint = Color.White, modifier = Modifier.size(40.dp))
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = null, tint = if (currentRoute == Screen.Home.route) Color(0xFFE50914) else Color.White) },
                    label = { Text("الرئيسية", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Home.route,
                    colors = NavigationDrawerItemDefaults.colors(
                        selectedContainerColor = Color(0xFFE50914).copy(alpha = 0.2f),
                        unselectedContainerColor = Color.Transparent
                    ),
                    shape = RoundedCornerShape(16.dp),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Home.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Download, contentDescription = null, tint = Color.White) },
                    label = { Text("التنزيلات", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Downloads.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Downloads.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Favorite, contentDescription = null, tint = Color.White) },
                    label = { Text("المكتبة", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Library.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Library.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )

                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Settings, contentDescription = null, tint = Color.White) },
                    label = { Text("الإعدادات", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.Settings.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.Settings.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.Outlined.Info, contentDescription = null, tint = Color.White) },
                    label = { Text("حول التطبيق", color = Color.White, fontSize = 16.sp) },
                    selected = currentRoute == Screen.About.route,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate(Screen.About.route)
                    },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                NavigationDrawerItem(
                    icon = { Icon(Icons.AutoMirrored.Filled.Help, contentDescription = null, tint = Color.White) },
                    label = { Text("مساعدة ودعم", color = Color.White, fontSize = 16.sp) },
                    selected = false,
                    colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                    onClick = { scope.launch { drawerState.close() } },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                Spacer(modifier = Modifier.weight(1f))
                
                HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))

                // Bottom Area (Logout)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 16.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .border(1.dp, Color(0xFF2A2A2E), RoundedCornerShape(12.dp))
                            .background(Color(0xFF161618))
                            .clickable { 
                                if (isGuest) {
                                    scope.launch { drawerState.close() }
                                    navController.navigate(Screen.Auth.route)
                                } else {
                                    scope.launch { drawerState.close() }
                                    showLogoutDialog = true
                                }
                            }
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(if (isGuest) "تسجيل الدخول" else "تسجيل الخروج", color = Color.White, fontSize = 16.sp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Icon(if (isGuest) Icons.Default.Person else Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log", tint = Color(0xFFE50914))
                    }
                }
            }
        }"""

pattern = re.compile(r'        drawerContent = \{.*?(?=    \) \{)', re.DOTALL)
new_content = pattern.sub(new_drawer + '\n', content)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(new_content)
