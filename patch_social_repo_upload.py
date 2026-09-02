import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

old_upload = """        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
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
        
        // Fallback to Firebase Storage
        val ref = FirebaseStorage.getInstance().reference.child("stories/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()"""

new_upload = """        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            try {
                try {
                    com.cloudinary.android.MediaManager.get()
                } catch (e: Exception) {
                    com.cloudinary.android.MediaManager.init(com.example.MyApplication.instance, mapOf("cloud_name" to cloudName))
                }
                
                val cloudinaryUrl = suspendCancellableCoroutine<String> { continuation ->
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
                return cloudinaryUrl
            } catch (e: Exception) {
                android.util.Log.e("Upload", "Cloudinary failed, falling back to Firebase", e)
            }
        }
        
        // Fallback to Firebase Storage
        val ref = FirebaseStorage.getInstance().reference.child("stories/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()"""

content = content.replace(old_upload, new_upload)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)

