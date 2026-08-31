import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# 1. Add showEditPhoto state
state_target = """    var showEditProfile by remember { mutableStateOf(false) }"""
state_replacement = """    var showEditProfile by remember { mutableStateOf(false) }
    var showEditPhoto by remember { mutableStateOf(false) }
    
    if (showEditPhoto) {
        AlertDialog(
            onDismissRequest = { showEditPhoto = false },
            title = { Text("Change Photo") },
            text = { Text("Coming soon...") },
            confirmButton = {
                TextButton(onClick = { showEditPhoto = false }) { Text("OK", color = primaryRed) }
            }
        )
    }"""
content = content.replace(state_target, state_replacement)

# 2. Change pencil icon action to showEditPhoto
pencil_target = """.clickable { showEditProfile = true },"""
pencil_replacement = """.clickable { showEditPhoto = true },"""
content = content.replace(pencil_target, pencil_replacement)

# 3. Make the account information clickable and update the text/remove "Member since May 2024"
# The section is:
info_target = """            Column(modifier = Modifier.weight(1f)) {
                val displayName = if (currentUser != null) {
                    "${currentUser?.firstName} ${currentUser?.lastName}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "User"
                } else {
                    "Guest User"
                }
                Text(displayName, color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                Text(currentUser?.email ?: "Sign in to access features", color = Color.Gray, fontSize = 14.sp)
                
                Spacer(modifier = Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Row(
                        modifier = Modifier.background(Color(0xFF301934), RoundedCornerShape(4.dp)).padding(horizontal = 6.dp, vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("👑", fontSize = 10.sp)
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Premium Plan", color = Color(0xFFFF5252), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Member since May 2024", color = Color.Gray, fontSize = 10.sp)
                }
            }"""

info_replacement = """            Column(
                modifier = Modifier
                    .weight(1f)
                    .clickable(enabled = currentUser != null) { showEditProfile = true }
                    .padding(vertical = 4.dp)
            ) {
                val displayName = if (currentUser != null) {
                    "${currentUser?.firstName} ${currentUser?.lastName}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "User"
                } else {
                    "Guest User"
                }
                Text(displayName, color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                if (currentUser != null && !currentUser?.username.isNullOrEmpty()) {
                    Text("@${currentUser?.username}", color = Color.LightGray, fontSize = 14.sp)
                }
                Text(currentUser?.email ?: "Sign in to access features", color = Color.Gray, fontSize = 14.sp)
                
                Spacer(modifier = Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Row(
                        modifier = Modifier.background(Color(0xFF301934), RoundedCornerShape(4.dp)).padding(horizontal = 6.dp, vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("👑", fontSize = 10.sp)
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Premium Plan", color = Color(0xFFFF5252), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }"""
content = content.replace(info_target, info_replacement)

# 4. Add Anime to Stats Row
stats_target = """        // Stats Row
        Row(
            modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp)).padding(16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            StatItem(Icons.Outlined.Movie, "24", "Movies", primaryRed)
            StatItem(Icons.Outlined.Tv, "12", "Series", primaryRed)
            StatItem(Icons.Outlined.FavoriteBorder, "18", "Watchlist", primaryRed)
            StatItem(Icons.Outlined.Download, "7", "Downloads", primaryRed)
        }"""
        
stats_replacement = """        // Stats Row
        Row(
            modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp)).padding(16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            StatItem(Icons.Outlined.Movie, "24", "Movies", primaryRed)
            StatItem(Icons.Outlined.Tv, "12", "Series", primaryRed)
            StatItem(Icons.Outlined.Face, "5", "Anime", primaryRed)
            StatItem(Icons.Outlined.FavoriteBorder, "18", "Watchlist", primaryRed)
            StatItem(Icons.Outlined.Download, "7", "Downloads", primaryRed)
        }"""
content = content.replace(stats_target, stats_replacement)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
