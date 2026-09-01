import re

with open("app/src/main/java/com/example/MyApplication.kt", "r") as f:
    content = f.read()

init_code = """
        super.onCreate()
        instance = this
        
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        if (cloudName.isNotEmpty()) {
            val config = mapOf(
                "cloud_name" to cloudName
            )
            try {
                com.cloudinary.android.MediaManager.init(this, config)
            } catch (e: Exception) {
                // Ignore if already initialized
            }
        }
"""

content = content.replace("        super.onCreate()\n        instance = this", init_code)

with open("app/src/main/java/com/example/MyApplication.kt", "w") as f:
    f.write(content)
