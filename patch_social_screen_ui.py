import re

with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'r') as f:
    content = f.read()

# Replace the direct sign-in logic
old_block = """                Button(
                    onClick = { signInWithGoogle() },
                    enabled = !isSigningIn,
                    modifier = Modifier.fillMaxWidth(0.8f).height(50.dp)
                ) {
                    if (isSigningIn) {
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                    } else {
                        Text("Sign in with Google")
                    }
                }
                
                if (BuildConfig.WEB_CLIENT_ID.isEmpty()) {
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Warning: WEB_CLIENT_ID not configured.", color = MaterialTheme.colorScheme.error, fontSize = 12.sp)
                }"""

new_block = """                Button(
                    onClick = { 
                        // Instead of signing in here, users should sign in through the Profile tab or Main Auth
                        // For simplicity, we just prompt them.
                    },
                    modifier = Modifier.fillMaxWidth(0.8f).height(50.dp)
                ) {
                    Text("Go to Profile to Sign In")
                }"""

content = content.replace(old_block, new_block)

# Remove the fun signInWithGoogle
content = re.sub(r'    fun signInWithGoogle\(\) \{.*?(?=        if \(currentUser == null\) \{)', '', content, flags=re.DOTALL)

# Remove unused imports
content = re.sub(r'import androidx.credentials.*?\n', '', content)
content = re.sub(r'import com.google.android.libraries.identity.googleid.*?\n', '', content)

with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'w') as f:
    f.write(content)
