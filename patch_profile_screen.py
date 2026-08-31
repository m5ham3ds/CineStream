import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add needed imports
imports_to_add = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.net.Uri
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
"""
content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\n" + imports_to_add)

# Change showEditPhoto logic to actually pick an image
edit_photo_logic_old = """    if (showEditPhoto) {
        AlertDialog(
            onDismissRequest = { showEditPhoto = false },
            title = { Text("Change Photo") },
            text = { Text("Coming soon...") },
            confirmButton = {
                TextButton(onClick = { showEditPhoto = false }) { Text("OK", color = primaryRed) }
            }
        )
    }"""

edit_photo_logic_new = """    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedImageUri = uri
            showEditProfile = true
        }
    }
    
    if (showEditPhoto) {
        LaunchedEffect(Unit) {
            photoPickerLauncher.launch("image/*")
            showEditPhoto = false
        }
    }"""
content = content.replace(edit_photo_logic_old, edit_photo_logic_new)

# Modify updateProfile call to include selectedImageUri
update_call_old = """                                    authViewModel.updateProfile(firstName, lastName, username) { success, error ->"""
update_call_new = """                                    authViewModel.updateProfile(firstName, lastName, username, selectedImageUri) { success, error ->"""
content = content.replace(update_call_old, update_call_new)

# Add selectedImageUri reset on success
reset_uri = """                                        showEditProfile = false
                                        Toast.makeText(context, "Profile updated", Toast.LENGTH_SHORT).show()"""
reset_uri_new = """                                        showEditProfile = false
                                        selectedImageUri = null
                                        Toast.makeText(context, "Profile updated", Toast.LENGTH_SHORT).show()"""
content = content.replace(reset_uri, reset_uri_new)

# Replace the Avatar Box to show AsyncImage if photoUrl or selectedImageUri exists
avatar_box_old = """            Box {
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(CircleShape)
                        .background(iconBgColor)
                        .border(2.dp, primaryRed, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    if (currentUser != null) {
                        Text(
                            text = (currentUser?.firstName?.take(1) ?: currentUser?.username?.take(1) ?: "U").uppercase(),
                            color = Color.White,
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Bold
                        )
                    } else {
                        Icon(Icons.Filled.Person, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(40.dp))
                    }
                }"""

avatar_box_new = """            Box {
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(CircleShape)
                        .background(iconBgColor)
                        .border(2.dp, primaryRed, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    if (selectedImageUri != null || (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true)) {
                        AsyncImage(
                            model = selectedImageUri ?: currentUser?.photoUrl,
                            contentDescription = "Profile Photo",
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                    } else if (currentUser != null) {
                        Text(
                            text = (currentUser?.firstName?.take(1) ?: currentUser?.username?.take(1) ?: "U").uppercase(),
                            color = Color.White,
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Bold
                        )
                    } else {
                        Icon(Icons.Filled.Person, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(40.dp))
                    }
                }"""
content = content.replace(avatar_box_old, avatar_box_new)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
