import re
import os

en_strings = """
    <string name="version_label">Version 1.0.0</string>
    <string name="last_updated">Last updated: May 25, 2024</string>
    <string name="our_mission">Our Mission</string>
    <string name="check_for_updates">Check for Updates</string>
    <string name="biography">Biography</string>
    <string name="top_movies">Top Movies</string>
    <string name="top_tv_shows">Top TV Shows</string>
    <string name="trailers">Trailers</string>
    <string name="no_watching_items">No items to watch</string>
    <string name="time_left">24m left of 48m</string>
"""

ar_strings = """
    <string name="version_label">الإصدار 1.0.0</string>
    <string name="last_updated">آخر تحديث: 25 مايو 2024</string>
    <string name="our_mission">مهمتنا</string>
    <string name="check_for_updates">التحقق من التحديثات</string>
    <string name="biography">السيرة الذاتية</string>
    <string name="top_movies">أفضل الأفلام</string>
    <string name="top_tv_shows">أفضل المسلسلات</string>
    <string name="trailers">المقاطع الدعائية</string>
    <string name="no_watching_items">لا توجد عناصر للمتابعة</string>
    <string name="time_left">متبقي 24 دقيقة من 48</string>
"""

def append_strings(file, new_strings):
    with open(file, 'r') as f:
        content = f.read()
    if '<string name="version_label">' not in content:
        content = content.replace('</resources>', new_strings.strip() + '\n</resources>')
        with open(file, 'w') as f:
            f.write(content)

append_strings('app/src/main/res/values/strings.xml', en_strings)
append_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

replacements = {
    r'Text\("Version 1.0.0"': 'Text(stringResource(R.string.version_label)',
    r'Text\("Last updated: May 25, 2024"': 'Text(stringResource(R.string.last_updated)',
    r'Text\("Our Mission"': 'Text(stringResource(R.string.our_mission)',
    r'Text\("Check for Updates"': 'Text(stringResource(R.string.check_for_updates)',
    r'Text\("Biography"': 'Text(stringResource(R.string.biography)',
    r'Text\("Top Movies"': 'Text(stringResource(R.string.top_movies)',
    r'Text\("Top TV Shows"': 'Text(stringResource(R.string.top_tv_shows)',
    r'Text\("Trailers"': 'Text(stringResource(R.string.trailers)',
    r'Text\("لا توجد عناصر للمتابعة"': 'Text(stringResource(R.string.no_watching_items)',
    r'Text\("24m left of 48m"': 'Text(stringResource(R.string.time_left)',
    r'Text\("No items to watch"': 'Text(stringResource(R.string.no_watching_items)'
}

for root, dirs, files in os.walk('app/src/main/java/com/example/ui'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            original = content
            for old, new in replacements.items():
                content = re.sub(old, new, content)
            
            if original != content:
                if 'import androidx.compose.ui.res.stringResource' not in content:
                    content = re.sub(r'(import [^\n]+)', r'\1\nimport androidx.compose.ui.res.stringResource\nimport com.example.R', content, count=1)
                with open(filepath, 'w') as f:
                    f.write(content)
