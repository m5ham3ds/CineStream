import re

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "r") as f:
    content = f.read()

bad_user_profile = """            UserProfile(user.uid, user.displayName ?: "User", user.photoUrl?.toString() ?: "", true)"""
fixed_user_profile = """            UserProfile(uid = user.uid, username = user.displayName ?: "User", photoUrl = user.photoUrl?.toString() ?: "", isOnline = true)"""

content = content.replace(bad_user_profile, fixed_user_profile)

with open("app/src/main/java/com/example/data/repository/SocialRepository.kt", "w") as f:
    f.write(content)
