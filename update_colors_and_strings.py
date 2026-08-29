import os
import re

# Update strings.xml
strings_en_path = 'app/src/main/res/values/strings.xml'
with open(strings_en_path, 'r') as f:
    strings_en = f.read()

if '<string name="movies">' not in strings_en:
    strings_en = strings_en.replace(
        '</resources>',
        '    <string name="movies">Movies</string>\n    <string name="series">Series</string>\n    <string name="anime">Anime</string>\n    <string name="library">Library</string>\n    <string name="profile">Profile</string>\n</resources>'
    )
    with open(strings_en_path, 'w') as f:
        f.write(strings_en)

# Update strings-ar.xml
strings_ar_path = 'app/src/main/res/values-ar/strings.xml'
with open(strings_ar_path, 'r') as f:
    strings_ar = f.read()

if '<string name="movies">' not in strings_ar:
    strings_ar = strings_ar.replace(
        '</resources>',
        '    <string name="movies">الأفلام</string>\n    <string name="series">المسلسلات</string>\n    <string name="anime">الأنمي</string>\n    <string name="library">المكتبة</string>\n    <string name="profile">الحساب</string>\n</resources>'
    )
    with open(strings_ar_path, 'w') as f:
        f.write(strings_ar)

# Update AppNavigation.kt manually
app_nav_path = 'app/src/main/java/com/example/navigation/AppNavigation.kt'
with open(app_nav_path, 'r') as f:
    app_nav = f.read()

# Fix the banner background
app_nav = app_nav.replace('if (updateFinishedShowGreen) Color(0xFF4CAF50) else primaryColorVal', 'if (updateFinishedShowGreen) Color(0xFF4CAF50) else Color(0xFFE50914)')
# Remove unused primaryColor variables
app_nav = re.sub(r'val primaryColor by userPrefs\.primaryColor\.collectAsState\(initial = 0\)\s*val primaryColorVal = [^\n]+\n', '', app_nav)

# Replace all remaining Color(0xFFE50914) with MaterialTheme.colorScheme.primary
app_nav = app_nav.replace('Color(0xFFE50914)', 'MaterialTheme.colorScheme.primary')
# Re-fix the banner one just in case the previous step caught it again... wait
# the previous replace 'Color(0xFFE50914)' will replace the one I just inserted for the banner!
# Let's fix that.
app_nav = app_nav.replace('if (updateFinishedShowGreen) Color(0xFF4CAF50) else MaterialTheme.colorScheme.primary', 'if (updateFinishedShowGreen) Color(0xFF4CAF50) else Color(0xFFE50914)')

if 'import androidx.compose.material3.MaterialTheme' not in app_nav:
    app_nav = app_nav.replace('import androidx.compose.material3.*', 'import androidx.compose.material3.*\nimport androidx.compose.material3.MaterialTheme')

with open(app_nav_path, 'w') as f:
    f.write(app_nav)

# Find all kt files
def process_file(filepath):
    if 'AppNavigation.kt' in filepath or 'Theme.kt' in filepath or 'Color.kt' in filepath:
        return # Skip these
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'Color(0xFFE50914)' in content:
        content = content.replace('Color(0xFFE50914)', 'MaterialTheme.colorScheme.primary')
        if 'import androidx.compose.material3.MaterialTheme' not in content and 'import androidx.compose.material3.*' not in content:
            # find first import
            content = re.sub(r'(import [^\n]+)', r'\1\nimport androidx.compose.material3.MaterialTheme', content, count=1)
        with open(filepath, 'w') as f:
            f.write(content)

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            process_file(os.path.join(root, file))
