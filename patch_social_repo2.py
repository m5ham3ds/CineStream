import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

old_upload = """    suspend fun uploadMedia(uri: Uri): String {
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        val uploadPreset = com.example.BuildConfig.CLOUDINARY_UPLOAD_PRESET
        
        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            return suspendCancellableCoroutine { continuation ->
                com.cloudinary.android.MediaManager.get().upload(uri)"""

new_upload = """    suspend fun uploadMedia(uri: Uri): String {
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        val uploadPreset = com.example.BuildConfig.CLOUDINARY_UPLOAD_PRESET
        
        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            try {
                com.cloudinary.android.MediaManager.get()
            } catch (e: Exception) {
                try {
                    com.cloudinary.android.MediaManager.init(com.example.MyApplication.instance, mapOf("cloud_name" to cloudName))
                } catch (e2: Exception) {
                    // Ignore
                }
            }
            return suspendCancellableCoroutine { continuation ->
                com.cloudinary.android.MediaManager.get().upload(uri)"""

content = content.replace(old_upload, new_upload)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
