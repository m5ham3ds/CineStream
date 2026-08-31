import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.screens.auth.AuthViewModel
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
"""
content = content.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\n" + imports)

# Get AuthViewModel
content = content.replace("    val userPrefs = remember", "    val authViewModel: AuthViewModel = viewModel()\n    val currentUser by authViewModel.currentUser.collectAsState()\n    val userPrefs = remember")

# Replace Drawer header
drawer_name_old = """                                Text(
                                    text = if (isGuest) "Guest User" else "E. Laurent","""
drawer_name_new = """                                val displayName = if (isGuest || currentUser == null) "Guest User" else {
                                    "${currentUser?.firstName} ${currentUser?.lastName}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "User"
                                }
                                Text(
                                    text = displayName,"""
content = content.replace(drawer_name_old, drawer_name_new)

# Replace Avatar in Drawer
drawer_avatar_old = """                            Box(
                                modifier = Modifier
                                    .size(70.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onSurfaceVariant)
                                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(40.dp))
                            }"""
drawer_avatar_new = """                            Box(
                                modifier = Modifier
                                    .size(70.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onSurfaceVariant)
                                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                if (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true) {
                                    AsyncImage(
                                        model = currentUser?.photoUrl,
                                        contentDescription = "Avatar",
                                        contentScale = ContentScale.Crop,
                                        modifier = Modifier.fillMaxSize()
                                    )
                                } else if (currentUser != null) {
                                    Text(
                                        text = (currentUser?.firstName?.take(1) ?: currentUser?.username?.take(1) ?: "U").uppercase(),
                                        color = MaterialTheme.colorScheme.onSurface,
                                        fontSize = 28.sp,
                                        fontWeight = FontWeight.Bold
                                    )
                                } else {
                                    Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(40.dp))
                                }
                            }"""
content = content.replace(drawer_avatar_old, drawer_avatar_new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
