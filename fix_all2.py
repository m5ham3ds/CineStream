import re

# Fix AuthScreen
with open('app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt', 'r') as f:
    auth_screen = f.read()

# Replace any lingering stringResource(R.string.xxx)
auth_screen = re.sub(r'stringResource\(R\.string\.[a-zA-Z_0-9]+\)', '""', auth_screen)

with open('app/src/main/java/com/example/ui/screens/auth/AuthScreen.kt', 'w') as f:
    f.write(auth_screen)


# Fix AuthViewModel
with open('app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt', 'r') as f:
    auth_vm = f.read()

auth_vm = auth_vm.replace('repository.auth.signInWithCredential(credential).kotlinx.coroutines.tasks.await()', 'repository.auth.signInWithCredential(credential).await()')
auth_vm = auth_vm.replace('repository.auth.signInWithEmailAndPassword(email, pass).kotlinx.coroutines.tasks.await()', 'repository.auth.signInWithEmailAndPassword(email, pass).await()')
auth_vm = auth_vm.replace('repository.auth.createUserWithEmailAndPassword(email, pass).kotlinx.coroutines.tasks.await()', 'repository.auth.createUserWithEmailAndPassword(email, pass).await()')
auth_vm = auth_vm.replace('repository.auth.sendPasswordResetEmail(email).kotlinx.coroutines.tasks.await()', 'repository.auth.sendPasswordResetEmail(email).await()')

with open('app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt', 'w') as f:
    f.write(auth_vm)


# Fix SocialViewModel
with open('app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt', 'r') as f:
    social_vm = f.read()

social_vm = social_vm.replace('repository.getCurrentUser()', 'SocialRepository().getCurrentUser()')
social_vm = social_vm.replace('repository.saveUserProfile()', 'SocialRepository().saveUserProfile()')
social_vm = social_vm.replace('repository.getMessages()', 'SocialRepository().getMessages()')
social_vm = social_vm.replace('repository.getStories()', 'SocialRepository().getStories()')
social_vm = social_vm.replace('repository.sendMessage(text)', 'SocialRepository().sendMessage(text)')
social_vm = social_vm.replace('repository.addStory(imageUrl)', 'SocialRepository().addStory(imageUrl)')

# Remove private val repository = SocialRepository() as it was getting confused
social_vm = social_vm.replace('private val repository = SocialRepository()', '')

with open('app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt', 'w') as f:
    f.write(social_vm)

# Fix SocialScreen
with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'r') as f:
    social_screen = f.read()

social_screen = social_screen.replace('.padding(0.dp)', '.padding(8.dp)')

with open('app/src/main/java/com/example/ui/screens/social/SocialScreen.kt', 'w') as f:
    f.write(social_screen)

