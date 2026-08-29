import re

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('@Composable\n}\nfun SettingsSectionHeader', '}\n\n@Composable\nfun SettingsSectionHeader')
content = content.replace('    }\n}\n\n@Composable\nfun SettingsSectionHeader', '    }\n}\n}\n\n@Composable\nfun SettingsSectionHeader')

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'w') as f:
    f.write(content)
