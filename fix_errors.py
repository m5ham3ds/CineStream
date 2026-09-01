import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

upload_old = """    suspend fun uploadProfilePicture(uid: String, uri: Uri): String? {
        return try {
            val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
            ref.putFile(uri).await()
            ref.downloadUrl.await().toString()
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }"""
upload_new = """    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
        val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()
    }"""
content = content.replace(upload_old, upload_new)
with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content2 = f.read()

viewmodel_old = """                    var finalPhotoUrl = currentUserData.photoUrl
                if (photoUri != null) {
                    val uploadedUrl = repository.uploadProfilePicture(currentUserData.uid, photoUri)
                    if (uploadedUrl != null) {
                        finalPhotoUrl = uploadedUrl
                    } else {
                        onComplete(false, "Failed to upload image. Check Firebase Storage rules or network.")
                        _isLoading.value = false
                        return@launch
                    }
                }

                val updatedUser = currentUserData.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = safeUsername,
                    photoUrl = finalPhotoUrl
                )
                kotlinx.coroutines.withTimeout(15000) { repository.saveUser(updatedUser) }
                _currentUser.value = updatedUser
                onComplete(true, null)
            } catch (e: Exception) {
                onComplete(false, "Failed to save to server. Check connection.")
            }"""

viewmodel_new = """                    var finalPhotoUrl = currentUserData.photoUrl
                if (photoUri != null) {
                    finalPhotoUrl = repository.uploadProfilePicture(currentUserData.uid, photoUri)
                }

                val updatedUser = currentUserData.copy(
                    firstName = firstName,
                    lastName = lastName,
                    username = safeUsername,
                    photoUrl = finalPhotoUrl
                )
                kotlinx.coroutines.withTimeout(15000) { repository.saveUser(updatedUser) }
                _currentUser.value = updatedUser
                onComplete(true, null)
            } catch (e: Exception) {
                onComplete(false, e.message ?: "Unknown error occurred")
            }"""
content2 = content2.replace(viewmodel_old, viewmodel_new)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content2)
