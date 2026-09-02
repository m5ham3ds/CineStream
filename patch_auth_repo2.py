import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

# Add flow imports
if "import kotlinx.coroutines.flow.MutableStateFlow" not in content:
    content = content.replace("import kotlinx.coroutines.tasks.await", "import kotlinx.coroutines.tasks.await\nimport kotlinx.coroutines.flow.MutableStateFlow\nimport kotlinx.coroutines.flow.StateFlow\nimport kotlinx.coroutines.flow.asStateFlow")

# Add currentUserFlow variable inside object AuthRepository
state_flow_code = """
    private val _currentUserFlow = MutableStateFlow<User?>(null)
    val currentUserFlow: StateFlow<User?> = _currentUserFlow.asStateFlow()
"""
if "val currentUserFlow" not in content:
    content = content.replace("object AuthRepository {\n", "object AuthRepository {\n" + state_flow_code)

# Modify getCurrentUser to update the flow
old_get = """    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser ?: return null
        return try {
            val snapshot = kotlinx.coroutines.withTimeout(15000) { db.collection("users").document(firebaseUser.uid).get().await() }
            if (snapshot.exists()) {
                snapshot.toObject(User::class.java)
            } else {
                null
            }
        } catch (e: Exception) {
            null
        }
    }"""

new_get = """    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser
        if (firebaseUser == null) {
            _currentUserFlow.value = null
            return null
        }
        return try {
            val snapshot = kotlinx.coroutines.withTimeout(15000) { db.collection("users").document(firebaseUser.uid).get().await() }
            if (snapshot.exists()) {
                val user = snapshot.toObject(User::class.java)
                _currentUserFlow.value = user
                user
            } else {
                _currentUserFlow.value = null
                null
            }
        } catch (e: Exception) {
            null
        }
    }"""
content = content.replace(old_get, new_get)

# Modify saveUser to update the flow
old_save = """    suspend fun saveUser(user: User) {
        db.collection("users").document(user.uid).set(user).await()
    }"""

new_save = """    suspend fun saveUser(user: User) {
        db.collection("users").document(user.uid).set(user).await()
        _currentUserFlow.value = user
    }"""
content = content.replace(old_save, new_save)

# Modify uploadProfilePicture to lazy init Cloudinary
old_upload = """    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        val uploadPreset = com.example.BuildConfig.CLOUDINARY_UPLOAD_PRESET
        
        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            return suspendCancellableCoroutine { continuation ->
                com.cloudinary.android.MediaManager.get().upload(uri)"""

new_upload = """    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
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

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
