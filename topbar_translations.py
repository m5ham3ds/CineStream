import re
import os

en_strings = """
    <string name="trending_title_first">Trending</string>
    <string name="trending_title_second">Now</string>
    <string name="trending_subtitle">See what\'s popular today</string>
    <string name="popular_title_first">Popular</string>
    <string name="popular_title_second">Picks</string>
    <string name="popular_subtitle">Most watched this week</string>
    <string name="upcoming_title_first">Coming</string>
    <string name="upcoming_title_second">Soon</string>
    <string name="upcoming_subtitle">Upcoming movies &amp; series</string>
    <string name="new_releases_title_first">New</string>
    <string name="new_releases_title_second">Releases</string>
    <string name="new_releases_subtitle">Latest additions</string>
    <string name="watching_title_first">Continue</string>
    <string name="watching_title_second">Watching</string>
    <string name="watching_subtitle">Pick up where you left off</string>
"""

ar_strings = """
    <string name="trending_title_first">رائج</string>
    <string name="trending_title_second">الآن</string>
    <string name="trending_subtitle">شاهد ما هو رائج اليوم</string>
    <string name="popular_title_first">اختيارات</string>
    <string name="popular_title_second">شائعة</string>
    <string name="popular_subtitle">الأكثر مشاهدة هذا الأسبوع</string>
    <string name="upcoming_title_first">قريباً</string>
    <string name="upcoming_title_second">جداً</string>
    <string name="upcoming_subtitle">الأفلام والمسلسلات القادمة</string>
    <string name="new_releases_title_first">أحدث</string>
    <string name="new_releases_title_second">الإصدارات</string>
    <string name="new_releases_subtitle">أحدث الإضافات</string>
    <string name="watching_title_first">متابعة</string>
    <string name="watching_title_second">المشاهدة</string>
    <string name="watching_subtitle">أكمل من حيث توقفت</string>
"""

def append_strings(file, new_strings):
    with open(file, 'r') as f:
        content = f.read()
    if '<string name="trending_title_first">' not in content:
        content = content.replace('</resources>', new_strings.strip() + '\n</resources>')
        with open(file, 'w') as f:
            f.write(content)

append_strings('app/src/main/res/values/strings.xml', en_strings)
append_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

replacements = {
    r'"Trending"': 'stringResource(R.string.trending_title_first)',
    r'"Now"': 'stringResource(R.string.trending_title_second)',
    r'"See what\'s popular today"': 'stringResource(R.string.trending_subtitle)',
    r'"Popular"': 'stringResource(R.string.popular_title_first)',
    r'"Picks"': 'stringResource(R.string.popular_title_second)',
    r'"Most watched this week"': 'stringResource(R.string.popular_subtitle)',
    r'"Coming"': 'stringResource(R.string.upcoming_title_first)',
    r'"Soon"': 'stringResource(R.string.upcoming_title_second)',
    r'"Upcoming movies & series"': 'stringResource(R.string.upcoming_subtitle)',
    r'"New"': 'stringResource(R.string.new_releases_title_first)',
    r'"Releases"': 'stringResource(R.string.new_releases_title_second)',
    r'"Latest additions"': 'stringResource(R.string.new_releases_subtitle)',
    r'"Continue"': 'stringResource(R.string.watching_title_first)',
    r'"Watching"': 'stringResource(R.string.watching_title_second)',
    r'"Pick up where you left off"': 'stringResource(R.string.watching_subtitle)'
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
