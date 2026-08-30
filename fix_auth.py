import os

filepath = 'app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

target = """                val googleIdOption = GetGoogleIdOption.Builder()
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
            }"""

replacement = """                val googleIdOption = GetGoogleIdOption.Builder()
                    .setFilterByAuthorizedAccounts(false)
                    .setServerClientId(webClientId)
                    .setAutoSelectEnabled(false) // Changed to false
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
                launch {
                    val apiKey = try { com.google.firebase.FirebaseApp.getInstance().options.apiKey } catch(ex: Exception) { "Unknown" }
                    android.widget.Toast.makeText(context, "G-Sign In Failed: ${e.message}\\nAPI Key: $apiKey", android.widget.Toast.LENGTH_LONG).show()
                }
            }"""

content = content.replace(target, replacement)
with open(filepath, 'w') as f:
    f.write(content)

