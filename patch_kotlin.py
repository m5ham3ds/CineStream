import re

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

if 'kotlinOptions' not in content:
    content = content.replace('compileOptions {', 'kotlinOptions {\n    jvmTarget = "11"\n  }\n  compileOptions {')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
