import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = content.replace('dependencies {\n', 'dependencies {\n  implementation(libs.cloudinary.android)\n')

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
