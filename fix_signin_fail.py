import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

email_signin_old = """                    } catch (e: Exception) {
                        // Network error or timeout. Do NOT overwrite.
                        _currentUser.value = repository.getCurrentUser() ?: User(uid = firebaseUser.uid, email = email)
                        _authError.value = "Warning: Could not sync profile data from server."
                    }"""

email_signin_new = """                    } catch (e: Exception) {
                        repository.auth.signOut()
                        _authError.value = "Network error: Could not load user profile. Please try again."
                        _currentUser.value = null
                    }"""

google_signin_old = """                    } catch (e: Exception) {
                        // Network error or timeout: don't overwrite! Just try to use whatever we can get locally, or wait.
                        _currentUser.value = repository.getCurrentUser() ?: User(uid = firebaseUser.uid, email = firebaseUser.email ?: "")
                        _authError.value = "Warning: Could not sync profile data from server."
                    }"""
google_signin_new = """                    } catch (e: Exception) {
                        repository.auth.signOut()
                        _authError.value = "Network error: Could not load user profile. Please try again."
                        _currentUser.value = null
                    }"""

content = content.replace(email_signin_old, email_signin_new)
content = content.replace(google_signin_old, google_signin_new)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)

