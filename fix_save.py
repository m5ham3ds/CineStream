import re

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# Fix updateProfile timeout and logic
update_old = """                kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(updatedUser) }
                _currentUser.value = updatedUser
                onComplete(true, null)
            } catch (e: Exception) {
                onComplete(false, e.message)
            } finally {
                _isLoading.value = false
            }"""

update_new = """                kotlinx.coroutines.withTimeout(15000) { repository.saveUser(updatedUser) }
                _currentUser.value = updatedUser
                onComplete(true, null)
            } catch (e: Exception) {
                onComplete(false, "Failed to save to server. Check connection.")
            } finally {
                _isLoading.value = false
            }"""

content = content.replace(update_old, update_new)

# Fix email signup timeout
signup_old = """                    try {
                        kotlinx.coroutines.withTimeoutOrNull(3000) { repository.saveUser(newUser) }
                    } catch (e: Exception) {}"""
signup_new = """                    try {
                        kotlinx.coroutines.withTimeout(15000) { repository.saveUser(newUser) }
                    } catch (e: Exception) {}"""
content = content.replace(signup_old, signup_new)

# Fix other withTimeoutOrNull(3000) to withTimeoutOrNull(15000)
content = content.replace("withTimeoutOrNull(3000)", "withTimeoutOrNull(15000)")

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
