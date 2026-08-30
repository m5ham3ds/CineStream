with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'r') as f:
    content = f.read()

# I used regex to remove `fun signInWithGoogle() { ... }` but maybe I left an extra brace.
# Let's count open and close braces.
open_braces = content.count('{')
close_braces = content.count('}')
print(f"SocialScreen: Open: {open_braces}, Close: {close_braces}")

with open('app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt', 'r') as f:
    content2 = f.read()
open_braces = content2.count('{')
close_braces = content2.count('}')
print(f"SocialViewModel: Open: {open_braces}, Close: {close_braces}")
