import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Fix header avatar
header_old = """                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(Color.DarkGray)
                                    .clickable {
                                         if (isGuest) {
                                            navController.navigate(Screen.Auth.route)
                                        } else {
                                            navController.navigate(Screen.Profile.route)
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                            }"""
header_new = """                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onSurfaceVariant)
                                    .clickable {
                                         if (isGuest) {
                                            navController.navigate(Screen.Auth.route)
                                        } else {
                                            navController.navigate(Screen.Profile.route)
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                if (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true) {
                                    AsyncImage(
                                        model = currentUser?.photoUrl,
                                        contentDescription = "Avatar",
                                        contentScale = ContentScale.Crop,
                                        modifier = Modifier.fillMaxSize()
                                    )
                                } else {
                                    Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.background)
                                }
                            }"""
content = content.replace(header_old, header_new)

# Fix drawer username
drawer_name_old = """                                Text(
                                    text = displayName,
                                    fontSize = 24.sp,
                                    fontFamily = FontFamily.SansSerif,
                                    color = MaterialTheme.colorScheme.onSurface
                                )"""
drawer_name_new = """                                Text(
                                    text = displayName,
                                    fontSize = 24.sp,
                                    fontFamily = FontFamily.SansSerif,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                if (!isGuest && currentUser?.username?.isNotBlank() == true) {
                                    Text(
                                        text = "@${currentUser?.username}",
                                        fontSize = 14.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }"""
content = content.replace(drawer_name_old, drawer_name_new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
