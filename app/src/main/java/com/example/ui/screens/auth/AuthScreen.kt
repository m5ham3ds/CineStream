package com.example.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import android.widget.Toast
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthScreen(
    onSkip: () -> Unit,
    onAuthSuccess: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val userPrefs = remember { com.example.data.repository.UserPreferencesRepository(context) }

    var isSignUp by remember { mutableStateOf(false) }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
            .padding(24.dp)
    ) {
        // Skip Button
        TextButton(
            onClick = { 
                scope.launch { userPrefs.saveIsGuest(true) }
                onSkip() 
            },
            modifier = Modifier.align(Alignment.TopEnd)
        ) {
            Text("Skip", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
        }

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.Center),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = if (isSignUp) "Create Account" else "Welcome Back",
                style = MaterialTheme.typography.headlineLarge,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )
            Spacer(modifier = Modifier.height(32.dp))

            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email (Gmail)") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = MaterialTheme.colorScheme.primary,
                    unfocusedBorderColor = Color.DarkGray,
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White
                )
            )
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = MaterialTheme.colorScheme.primary,
                    unfocusedBorderColor = Color.DarkGray,
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White
                )
            )
            Spacer(modifier = Modifier.height(16.dp))

            var agreeToTerms by remember { mutableStateOf(false) }

            if (isSignUp) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Checkbox(
                        checked = agreeToTerms,
                        onCheckedChange = { agreeToTerms = it },
                        colors = CheckboxDefaults.colors(
                            checkedColor = MaterialTheme.colorScheme.primary,
                            uncheckedColor = Color.Gray
                        )
                    )
                    Text("I agree to Terms & Conditions", color = Color.White)
                }
            } else {
                TextButton(
                    onClick = { Toast.makeText(context, "Forgot Password clicked", Toast.LENGTH_SHORT).show() },
                    modifier = Modifier.align(Alignment.End)
                ) {
                    Text("Forgot Password?", color = MaterialTheme.colorScheme.primary)
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = { 
                    if (isSignUp && !agreeToTerms) {
                        Toast.makeText(context, "Please agree to terms", Toast.LENGTH_SHORT).show()
                        return@Button
                    }
                    if (email.isNotBlank() && password.isNotBlank()) {
                        scope.launch { 
                            userPrefs.saveIsGuest(false) 
                            userPrefs.saveIsLoggedIn(true)
                        }
                        onAuthSuccess() 
                    } else {
                        Toast.makeText(context, "Please enter email and password", Toast.LENGTH_SHORT).show()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                shape = RoundedCornerShape(8.dp)
            ) {
                Text(if (isSignUp) "Sign Up" else "Sign In")
            }

            Spacer(modifier = Modifier.height(24.dp))
            Text("Or continue with", color = Color.Gray)
            Spacer(modifier = Modifier.height(24.dp))

            // Google Sign In Button
            Button(
                onClick = { 
                    Toast.makeText(context, "Google Sign-In logic goes here.", Toast.LENGTH_SHORT).show()
                    scope.launch { 
                        userPrefs.saveIsGuest(false) 
                        userPrefs.saveIsLoggedIn(true)
                    }
                    onAuthSuccess()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                shape = RoundedCornerShape(8.dp)
            ) {
                Text("Sign in with Google", color = Color.Black, fontWeight = FontWeight.Bold)
            }

            Spacer(modifier = Modifier.height(32.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = if (isSignUp) "Already have an account?" else "Don't have an account?",
                    color = Color.LightGray
                )
                TextButton(onClick = { isSignUp = !isSignUp }) {
                    Text(if (isSignUp) "Sign In" else "Sign Up", color = MaterialTheme.colorScheme.primary)
                }
            }
        }
    }
}
