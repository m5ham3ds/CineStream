with open('app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt', 'r') as f:
    content = f.read()
open_braces = content.count('{')
close_braces = content.count('}')
print(f"AuthScreen: Open: {open_braces}, Close: {close_braces}")

with open('app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt', 'r') as f:
    content2 = f.read()
open_braces = content2.count('{')
close_braces = content2.count('}')
print(f"ProfileScreen: Open: {open_braces}, Close: {close_braces}")
