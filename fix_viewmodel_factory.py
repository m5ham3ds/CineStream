import re
with open('app/src/main/java/com/example/ui/ViewModelFactory.kt', 'r') as f:
    c = f.read()

new_block = """        if (modelClass.isAssignableFrom(AnimeViewModel::class.java)) {
            return AnimeViewModel(AppContainer.mediaRepository) as T
        }
        if (modelClass.isAssignableFrom(com.example.ui.screens.social.SocialViewModel::class.java)) {
            return com.example.ui.screens.social.SocialViewModel() as T
        }"""

c = c.replace("""        if (modelClass.isAssignableFrom(AnimeViewModel::class.java)) {
            return AnimeViewModel(AppContainer.mediaRepository) as T
        }""", new_block)

with open('app/src/main/java/com/example/ui/ViewModelFactory.kt', 'w') as f:
    f.write(c)
