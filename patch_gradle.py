import re

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

# Add jsoup
if 'implementation(libs.jsoup)' not in content:
    content = content.replace('implementation(libs.okhttp)', 'implementation(libs.okhttp)\n  implementation(libs.jsoup)')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
