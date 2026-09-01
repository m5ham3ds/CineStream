import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Fix photo picker logic
content = content.replace("showEditProfile = true", "showImageConfirmDialog = true")
content = content.replace("var showEditPhoto by remember { mutableStateOf(false) }", "var showEditPhoto by remember { mutableStateOf(false) }\n    var showImageConfirmDialog by remember { mutableStateOf(false) }\n    var showLogoutConfirm by remember { mutableStateOf(false) }")

# Replace sign out logic
sign_out_btn_old = """onClick = { 
                    authViewModel.signOut()
                    onNavigateToAuth()
                }"""
sign_out_btn_new = """onClick = { showLogoutConfirm = true }"""
content = content.replace(sign_out_btn_old, sign_out_btn_new)
content = content.replace("onClick = { authViewModel.signOut() }", "onClick = { showLogoutConfirm = true }")

# Add dialogs
dialogs = """
    if (showLogoutConfirm) {
        AlertDialog(
            onDismissRequest = { showLogoutConfirm = false },
            title = { Text("Sign Out", color = Color.White) },
            text = { Text("Are you sure you want to sign out?", color = Color.Gray) },
            confirmButton = {
                TextButton(
                    onClick = {
                        showLogoutConfirm = false
                        authViewModel.signOut()
                        onNavigateToAuth()
                    }
                ) { Text("Sign Out", color = primaryRed) }
            },
            dismissButton = {
                TextButton(onClick = { showLogoutConfirm = false }) { Text("Cancel", color = Color.White) }
            },
            containerColor = cardColor
        )
    }

    if (showImageConfirmDialog && selectedImageUri != null) {
        AlertDialog(
            onDismissRequest = { 
                showImageConfirmDialog = false 
                selectedImageUri = null
            },
            title = { Text("Update Profile Picture", color = Color.White) },
            text = { 
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    AsyncImage(
                        model = selectedImageUri,
                        contentDescription = "New Profile Photo",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.size(120.dp).clip(CircleShape).border(2.dp, primaryRed, CircleShape)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Do you want to set this as your new profile picture?", color = Color.Gray)
                    if (isLoading) {
                        Spacer(modifier = Modifier.height(16.dp))
                        CircularProgressIndicator(color = primaryRed)
                    }
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        authViewModel.updateProfile(
                            currentUser?.firstName ?: "", 
                            currentUser?.lastName ?: "", 
                            currentUser?.username ?: "", 
                            selectedImageUri
                        ) { success, error ->
                            if (success) {
                                showImageConfirmDialog = false
                                selectedImageUri = null
                                Toast.makeText(context, "Profile picture updated", Toast.LENGTH_SHORT).show()
                            } else {
                                Toast.makeText(context, error ?: "Failed to update", Toast.LENGTH_SHORT).show()
                            }
                        }
                    },
                    enabled = !isLoading
                ) { Text("Save", color = primaryRed) }
            },
            dismissButton = {
                TextButton(
                    onClick = { 
                        showImageConfirmDialog = false 
                        selectedImageUri = null
                    },
                    enabled = !isLoading
                ) { Text("Cancel", color = Color.White) }
            },
            containerColor = cardColor
        )
    }
"""

content = content.replace("if (showEditProfile && currentUser != null) {", dialogs + "\n    if (showEditProfile && currentUser != null) {")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
