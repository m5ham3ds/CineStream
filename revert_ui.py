import os

auth_code = """package com.example.ui.screens.auth

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material.icons.outlined.Email
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.launch
import com.example.ui.ViewModelFactory
import androidx.credentials.CredentialManager
import androidx.credentials.GetCredentialRequest
import androidx.credentials.exceptions.GetCredentialException
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.example.BuildConfig
import com.example.data.repository.UserPreferencesRepository

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthScreen(
    onSkip: () -> Unit,
    onAuthSuccess: () -> Unit,
    userPrefs: UserPreferencesRepository = UserPreferencesRepository(LocalContext.current)
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val authViewModel: AuthViewModel = viewModel(factory = ViewModelFactory())
    val currentUser by authViewModel.currentUser.collectAsState()
    val authError by authViewModel.authError.collectAsState()
    val isLoading by authViewModel.isLoading.collectAsState()

    var isSignUp by remember { mutableStateOf(false) }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }
    var rememberMe by remember { mutableStateOf(false) }
    var showForgotPasswordDialog by remember { mutableStateOf(false) }

    val primaryRed = Color(0xFFE50914)
    val bgColor = Color(0xFF121212)
    val cardColor = Color(0xFF1E1E1E)

    LaunchedEffect(currentUser) {
        if (currentUser != null) {
            userPrefs.saveIsGuest(false)
            userPrefs.saveIsLoggedIn(true)
            onAuthSuccess()
        }
    }

    LaunchedEffect(authError) {
        authError?.let {
            Toast.makeText(context, it, Toast.LENGTH_LONG).show()
            authViewModel.resetError()
        }
    }

    fun signInWithGoogle() {
        val webClientId = BuildConfig.WEB_CLIENT_ID
        if (webClientId.isEmpty()) {
            Toast.makeText(context, "Google Sign-In not configured", Toast.LENGTH_SHORT).show()
            return
        }
        scope.launch {
            try {
                val credentialManager = CredentialManager.create(context)
                val googleIdOption = GetGoogleIdOption.Builder()
                    .setFilterByAuthorizedAccounts(false)
                    .setServerClientId(webClientId)
                    .setAutoSelectEnabled(true)
                    .build()
                val request = GetCredentialRequest.Builder()
                    .addCredentialOption(googleIdOption)
                    .build()
                val result = credentialManager.getCredential(context, request)
                val credential = result.credential
                
                if (credential is GoogleIdTokenCredential) {
                    authViewModel.handleGoogleSignIn(
                        idToken = credential.idToken,
                        email = credential.id,
                        displayName = credential.displayName,
                        photoUrl = credential.profilePictureUri?.toString()
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    if (showForgotPasswordDialog) {
        var resetEmail by remember { mutableStateOf(email) }
        AlertDialog(
            onDismissRequest = { showForgotPasswordDialog = false },
            title = { Text("Reset Password") },
            text = {
                OutlinedTextField(
                    value = resetEmail,
                    onValueChange = { resetEmail = it },
                    placeholder = { Text("Enter your email") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (resetEmail.isNotBlank()) {
                        authViewModel.resetPassword(resetEmail)
                        showForgotPasswordDialog = false
                    }
                }) {
                    Text("Send", color = primaryRed)
                }
            },
            dismissButton = {
                TextButton(onClick = { showForgotPasswordDialog = false }) {
                    Text("Cancel", color = Color.Gray)
                }
            }
        )
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
    ) {
        // Skip Button
        Text(
            text = "Skip",
            color = primaryRed,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 48.dp, end = 24.dp)
                .clickable {
                    scope.launch {
                        userPrefs.saveIsGuest(true)
                        userPrefs.saveIsLoggedIn(false)
                        onSkip()
                    }
                }
        )

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.Center)
                .padding(horizontal = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "CineStream",
                color = primaryRed,
                fontFamily = FontFamily.Serif,
                fontWeight = FontWeight.ExtraBold,
                fontSize = 42.sp
            )
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = if (isSignUp) "Create Account" else "Welcome Back!",
                color = Color.White,
                fontWeight = FontWeight.Bold,
                fontSize = 28.sp
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = if (isSignUp) "Sign up to start your cinematic journey" else "Sign in to continue your cinematic journey",
                color = Color.Gray,
                fontSize = 14.sp
            )
            Spacer(modifier = Modifier.height(32.dp))

            // Input Card
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(cardColor, RoundedCornerShape(16.dp))
                    .padding(24.dp)
            ) {
                OutlinedTextField(
                    value = email,
                    onValueChange = { email = it },
                    placeholder = { Text("Email (Gmail)", color = Color.Gray) },
                    leadingIcon = { Icon(Icons.Outlined.Email, contentDescription = null, tint = primaryRed) },
                    singleLine = true,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Gray,
                        unfocusedBorderColor = Color.DarkGray,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        cursorColor = primaryRed
                    ),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(8.dp)
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    placeholder = { Text("Password", color = Color.Gray) },
                    leadingIcon = { Icon(Icons.Outlined.Lock, contentDescription = null, tint = primaryRed) },
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                imageVector = if (passwordVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff,
                                contentDescription = null,
                                tint = Color.Gray
                            )
                        }
                    },
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    singleLine = true,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Gray,
                        unfocusedBorderColor = Color.DarkGray,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        cursorColor = primaryRed
                    ),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(8.dp)
                )
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(
                            checked = rememberMe,
                            onCheckedChange = { rememberMe = it },
                            colors = CheckboxDefaults.colors(
                                checkedColor = primaryRed,
                                uncheckedColor = Color.Gray,
                                checkmarkColor = Color.White
                            )
                        )
                        Text("Remember me", color = Color.Gray, fontSize = 14.sp)
                    }
                    if (!isSignUp) {
                        Text(
                            text = "Forgot Password?",
                            color = primaryRed,
                            fontSize = 14.sp,
                            modifier = Modifier.clickable { showForgotPasswordDialog = true }
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                Button(
                    onClick = {
                        if (email.isNotBlank() && password.isNotBlank()) {
                            if (isSignUp) {
                                authViewModel.signUpWithEmail(email, password)
                            } else {
                                authViewModel.signInWithEmail(email, password)
                            }
                        } else {
                            Toast.makeText(context, "Please enter email and password", Toast.LENGTH_SHORT).show()
                        }
                    },
                    modifier = Modifier.fillMaxWidth().height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = primaryRed),
                    shape = RoundedCornerShape(8.dp),
                    enabled = !isLoading
                ) {
                    if (isLoading) {
                        CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                    } else {
                        Text(if (isSignUp) "Sign Up" else "Sign In", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                HorizontalDivider(modifier = Modifier.weight(1f), color = Color.DarkGray)
                Text("Or continue with", color = Color.Gray, fontSize = 14.sp, modifier = Modifier.padding(horizontal = 16.dp))
                HorizontalDivider(modifier = Modifier.weight(1f), color = Color.DarkGray)
            }
            Spacer(modifier = Modifier.height(32.dp))
            
            Button(
                onClick = { signInWithGoogle() },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                shape = RoundedCornerShape(8.dp),
                enabled = !isLoading
            ) {
                Text("G ", color = Color.Black, fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
                Text("Sign in with Google", color = Color.Black, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            }

            Spacer(modifier = Modifier.height(32.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = if (isSignUp) "Already have an account? " else "Don't have an account? ",
                    color = Color.Gray,
                    fontSize = 14.sp
                )
                Text(
                    text = if (isSignUp) "Sign In" else "Sign Up",
                    color = primaryRed,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.clickable { isSignUp = !isSignUp }
                )
            }
        }
    }
}
"""

profile_code = """package com.example.ui.screens.profile

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.ui.ViewModelFactory
import com.example.ui.screens.auth.AuthViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen() {
    val authViewModel: AuthViewModel = viewModel(factory = ViewModelFactory())
    val currentUser by authViewModel.currentUser.collectAsState()
    val isLoading by authViewModel.isLoading.collectAsState()
    val context = LocalContext.current

    var showEditProfile by remember { mutableStateOf(false) }

    val primaryRed = Color(0xFFE50914)
    val bgColor = Color(0xFF121212)
    val cardColor = Color(0xFF1E1E1E)
    val iconBgColor = Color(0xFF2C2C2E)

    if (showEditProfile && currentUser != null) {
        var firstName by remember { mutableStateOf(currentUser?.firstName ?: "") }
        var lastName by remember { mutableStateOf(currentUser?.lastName ?: "") }
        var username by remember { mutableStateOf(currentUser?.username ?: "") }
        
        AlertDialog(
            onDismissRequest = { showEditProfile = false },
            title = { Text("Edit Profile") },
            text = {
                Column {
                    OutlinedTextField(
                        value = firstName,
                        onValueChange = { firstName = it },
                        label = { Text("First Name") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                    )
                    OutlinedTextField(
                        value = lastName,
                        onValueChange = { lastName = it },
                        label = { Text("Last Name") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                    )
                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it },
                        label = { Text("Username") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                    )
                    if (isLoading) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(top = 8.dp), color = primaryRed)
                    }
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (username.isNotBlank()) {
                            authViewModel.updateProfile(firstName, lastName, username) { success, error ->
                                if (success) {
                                    showEditProfile = false
                                    Toast.makeText(context, "Profile updated", Toast.LENGTH_SHORT).show()
                                } else {
                                    Toast.makeText(context, error ?: "Failed to update", Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    },
                    enabled = !isLoading
                ) {
                    Text("Save", color = primaryRed)
                }
            },
            dismissButton = {
                TextButton(onClick = { showEditProfile = false }, enabled = !isLoading) {
                    Text("Cancel", color = Color.Gray)
                }
            }
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        // Header
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box {
                Box(
                    modifier = Modifier.size(80.dp).clip(CircleShape).background(iconBgColor),
                    contentAlignment = Alignment.Center
                ) {
                    if (!currentUser?.photoUrl.isNullOrEmpty()) {
                        AsyncImage(
                            model = currentUser?.photoUrl,
                            contentDescription = null,
                            modifier = Modifier.fillMaxSize().clip(CircleShape)
                        )
                    } else {
                        Icon(Icons.Outlined.Person, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(40.dp))
                    }
                }
                if (currentUser != null) {
                    Box(
                        modifier = Modifier
                            .align(Alignment.BottomEnd)
                            .size(24.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF3A3A3C))
                            .clickable { showEditProfile = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Filled.Edit, contentDescription = "Edit", tint = Color.White, modifier = Modifier.size(14.dp))
                    }
                }
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
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
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Stats Row
        Row(
            modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp)).padding(16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            StatItem(Icons.Outlined.Movie, "24", "Movies", primaryRed)
            StatItem(Icons.Outlined.Tv, "12", "Series", primaryRed)
            StatItem(Icons.Outlined.FavoriteBorder, "18", "Watchlist", primaryRed)
            StatItem(Icons.Outlined.Download, "7", "Downloads", primaryRed)
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Premium Banner
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, primaryRed.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
                .background(cardColor, RoundedCornerShape(12.dp))
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier.size(48.dp).clip(CircleShape).background(iconBgColor),
                contentAlignment = Alignment.Center
            ) {
                Text("👑", fontSize = 24.sp)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text("You're Premium!", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(4.dp))
                Text("Enjoy ad-free streaming and exclusive content.", color = Color.Gray, fontSize = 12.sp, lineHeight = 16.sp)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Button(
                onClick = {},
                colors = ButtonDefaults.buttonColors(containerColor = primaryRed),
                shape = RoundedCornerShape(24.dp),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Text("Manage Plan", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Account
        Text("Account", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Outlined.Person, "Account Information", "Update your personal details", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.Security, "Security", "Password, device management", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.CreditCard, "Subscription", "Manage your plan and billing", true, primaryRed, iconBgColor)
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Preferences
        Text("Preferences", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Outlined.Settings, "App Settings", "Customize your experience", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.PlayCircleOutline, "Playback", "Quality, subtitles, autoplay", false, primaryRed, iconBgColor)
            ProfileListItem(Icons.Outlined.Notifications, "Notifications", "Manage your notification preferences", true, primaryRed, iconBgColor)
        }
        
        if (currentUser != null) {
            Spacer(modifier = Modifier.height(32.dp))
            Button(
                onClick = { authViewModel.signOut() },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2C2C2E)),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Sign Out", color = primaryRed, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            }
        }

        Spacer(modifier = Modifier.height(100.dp))
    }
}

@Composable
fun StatItem(icon: ImageVector, count: String, label: String, tintColor: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.height(8.dp))
        Text(count, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, color = Color.Gray, fontSize = 12.sp)
    }
}

@Composable
fun ProfileListItem(icon: ImageVector, title: String, subtitle: String, isLast: Boolean, tintColor: Color, iconBg: Color) {
    Row(
        modifier = Modifier.fillMaxWidth().clickable { }.padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier.size(40.dp).clip(CircleShape).background(iconBg),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(20.dp))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, color = Color.Gray, fontSize = 12.sp)
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
    }
    if (!isLast) {
        HorizontalDivider(modifier = Modifier.padding(start = 72.dp), color = Color(0xFF2C2C2E))
    }
}
"""

with open('app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt', 'w') as f:
    f.write(auth_code)

with open('app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt', 'w') as f:
    f.write(profile_code)
