import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

replacements = {
    'drawerContainerColor = Color(0xFF161618)': 'drawerContainerColor = MaterialTheme.colorScheme.surface',
    'listOf(Color(0xFF2B2B2B), Color(0xFF161618))': 'listOf(MaterialTheme.colorScheme.surfaceVariant, MaterialTheme.colorScheme.surface)',
    'tint = Color.White': 'tint = MaterialTheme.colorScheme.onSurface',
    'color = Color.White': 'color = MaterialTheme.colorScheme.onSurface',
    'Color(0xFF2A2A2E)': 'MaterialTheme.colorScheme.surfaceVariant',
    'Color(0xFF161618)': 'MaterialTheme.colorScheme.surface',
    'containerColor = Color(0xFF1E1E20)': 'containerColor = MaterialTheme.colorScheme.surface',
    'titleContentColor = Color.White': 'titleContentColor = MaterialTheme.colorScheme.onSurface',
    'containerColor = Color.Black': 'containerColor = MaterialTheme.colorScheme.background',
    'contentColor = Color.White': 'contentColor = MaterialTheme.colorScheme.onPrimary'
}

for old, new in replacements.items():
    content = content.replace(old, new)

# specific fix for the notification badge text color which might be in red primary color
# wait, red badge with text color? 
# contentColor = MaterialTheme.colorScheme.onPrimary is better.
# And the banner text
content = content.replace('color = MaterialTheme.colorScheme.onSurface,\n                                fontSize = 12.sp,\n                                fontWeight = FontWeight.Bold', 'color = Color.White,\n                                fontSize = 12.sp,\n                                fontWeight = FontWeight.Bold') # revert banner text to white since banner is red/green

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)

