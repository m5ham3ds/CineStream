import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

new_route = """    object EditProfile : Screen("edit_profile", "Edit Profile", Icons.Default.Person)
    object PublicProfile : Screen("public_profile/{userId}", "Public Profile", Icons.Default.Person) {
        fun createRoute(userId: String) = "public_profile/$userId"
    }"""

content = content.replace('    object EditProfile : Screen("edit_profile", "Edit Profile", Icons.Default.Person)', new_route)

with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
    f.write(content)

