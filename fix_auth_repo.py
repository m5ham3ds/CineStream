import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

# Add imports at the top
if "import kotlinx.coroutines.suspendCancellableCoroutine" not in content:
    content = content.replace("import kotlinx.coroutines.tasks.await", "import kotlinx.coroutines.tasks.await\nimport kotlinx.coroutines.suspendCancellableCoroutine\nimport kotlin.coroutines.resume\nimport kotlin.coroutines.resumeWithException")

old_upload = """    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
        val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()
    }"""

new_upload = """    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        val uploadPreset = com.example.BuildConfig.CLOUDINARY_UPLOAD_PRESET
        
        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            return suspendCancellableCoroutine { continuation ->
                com.cloudinary.android.MediaManager.get().upload(uri)
                    .unsigned(uploadPreset)
                    .callback(object : com.cloudinary.android.callback.UploadCallback {
                        override fun onSuccess(requestId: String?, resultData: Map<*, *>?) {
                            val secureUrl = resultData?.get("secure_url") as? String
                            if (secureUrl != null) {
                                continuation.resume(secureUrl)
                            } else {
                                continuation.resumeWithException(Exception("Secure URL not found"))
                            }
                        }
                        
                        override fun onStart(requestId: String?) {}
                        override fun onProgress(requestId: String?, bytes: Long, totalBytes: Long) {}
                        override fun onError(requestId: String?, error: com.cloudinary.android.callback.ErrorInfo?) {
                            continuation.resumeWithException(Exception(error?.description ?: "Unknown error"))
                        }
                        override fun onReschedule(requestId: String?, error: com.cloudinary.android.callback.ErrorInfo?) {}
                    }).dispatch()
            }
        }
        
        // Fallback to Firebase Storage if Cloudinary is not configured
        val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()
    }"""

content = content.replace(old_upload, new_upload)

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
