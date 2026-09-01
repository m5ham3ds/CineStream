import re

with open("gradle/libs.versions.toml", "r") as f:
    content = f.read()

content = content.replace('[versions]\n', '[versions]\ncloudinary = "2.5.0"\n')
content = content.replace('[libraries]\n', '[libraries]\ncloudinary-android = { module = "com.cloudinary:cloudinary-android", version.ref = "cloudinary" }\n')

with open("gradle/libs.versions.toml", "w") as f:
    f.write(content)
