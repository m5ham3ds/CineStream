import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    content = f.read()

# Replace the inner models
target_chats = """    val chats = listOf(
        SocialScreenChatMock("Ahmed", "Hey! How are you doing?", "12:45 PM", 2, true),
        SocialScreenChatMock("Sara", "Let's watch this tonight 🔥", "11:30 AM", 1, true),
        SocialScreenChatMock("Ali", "Thanks! I'll check it out.", "Yesterday", 0, false),
        SocialScreenChatMock("Movie Buddies", "Mohamed: That was insane!", "Yesterday", 0, true, true),
        SocialScreenChatMock("Mohamed", "See you tomorrow!", "Mon", 0, false),
        SocialScreenChatMock("Nour", "Sent a photo", "Sun", 0, false)
    )"""

replacement_chats = """    val chats = listOf(
        SocialScreenChatMock("Ahmed", "Hey! How are you doing?", "12:45 PM", 2, true, false),
        SocialScreenChatMock("Sara", "Let's watch this tonight 🔥", "11:30 AM", 1, true, false),
        SocialScreenChatMock("Ali", "Thanks! I'll check it out.", "Yesterday", 0, false, false),
        SocialScreenChatMock("Movie Buddies", "Mohamed: That was insane!", "Yesterday", 0, true, true),
        SocialScreenChatMock("Mohamed", "See you tomorrow!", "Mon", 0, false, false),
        SocialScreenChatMock("Nour", "Sent a photo", "Sun", 0, false, false)
    )"""
content = content.replace(target_chats, replacement_chats)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(content)
