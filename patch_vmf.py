import re

with open('app/src/main/java/com/example/ui/ViewModelFactory.kt', 'r') as f:
    content = f.read()

content = content.replace('throw IllegalArgumentException("Unknown ViewModel class")', 
'''        if (modelClass.isAssignableFrom(com.example.ui.screens.auth.AuthViewModel::class.java)) {
            return com.example.ui.screens.auth.AuthViewModel() as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")''')

with open('app/src/main/java/com/example/ui/ViewModelFactory.kt', 'w') as f:
    f.write(content)
