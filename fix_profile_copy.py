import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Replace the text of the username to be clickable and copy it.
# Need to import LocalClipboardManager and ClipboardManager? Yes, or just use context.
# Let's use context.getSystemService(Context.CLIPBOARD_SERVICE)

old_username_text = """                if (currentUser != null && !currentUser?.username.isNullOrEmpty()) {
                    Text("@${currentUser?.username}", color = Color.LightGray, fontSize = 14.sp)
                }"""

new_username_text = """                if (currentUser != null && !currentUser?.username.isNullOrEmpty()) {
                    Text(
                        text = "@${currentUser?.username}",
                        color = Color.LightGray,
                        fontSize = 14.sp,
                        modifier = Modifier
                            .clip(RoundedCornerShape(4.dp))
                            .clickable {
                                val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                val clip = android.content.ClipData.newPlainText("username", currentUser?.username)
                                clipboard.setPrimaryClip(clip)
                                Toast.makeText(context, "Username copied", Toast.LENGTH_SHORT).show()
                            }
                            .padding(2.dp)
                    )
                }"""

content = content.replace(old_username_text, new_username_text)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
