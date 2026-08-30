import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Just print the imports to see them
lines = content.split('\n')
for line in lines[:50]:
    print(line)

