import re
import os

en_strings = """
    <string name="trending_now">Trending Now</string>
    <string name="continue_watching">Continue Watching</string>
    <string name="trending_series">Trending Series</string>
    <string name="anime">Anime</string>
    <string name="coming_soon">Coming Soon</string>
    <string name="new_releases">New Releases</string>
    <string name="popular_series">Popular Series</string>
    <string name="popular_movies">Popular Movies</string>
    <string name="popular_anime">Popular Anime</string>
    <string name="popular_searches">Popular Searches</string>
    <string name="recent_searches">Recent Searches</string>
    <string name="clear_all">Clear All</string>
    <string name="edit_action">Edit ></string>
    <string name="see_all">See All</string>
    <string name="movies">Movies</string>
    <string name="series">Series</string>
    <string name="all">All</string>
    <string name="trending">Trending</string>
    <string name="popular">Popular</string>
"""

ar_strings = """
    <string name="trending_now">رائج الآن</string>
    <string name="continue_watching">متابعة المشاهدة</string>
    <string name="trending_series">مسلسلات رائجة</string>
    <string name="anime">أنمي</string>
    <string name="coming_soon">قريباً</string>
    <string name="new_releases">أحدث الإصدارات</string>
    <string name="popular_series">مسلسلات شهيرة</string>
    <string name="popular_movies">أفلام شهيرة</string>
    <string name="popular_anime">أنمي شهير</string>
    <string name="popular_searches">عمليات البحث الشائعة</string>
    <string name="recent_searches">عمليات البحث الأخيرة</string>
    <string name="clear_all">مسح الكل</string>
    <string name="edit_action">تعديل ></string>
    <string name="see_all">عرض الكل</string>
    <string name="movies">أفلام</string>
    <string name="series">مسلسلات</string>
    <string name="all">الكل</string>
    <string name="trending">رائج</string>
    <string name="popular">شائع</string>
"""

def append_strings(file, new_strings):
    with open(file, 'r') as f:
        content = f.read()
    if '<string name="trending_now">' not in content:
        content = content.replace('</resources>', new_strings.strip() + '\n</resources>')
        with open(file, 'w') as f:
            f.write(content)

append_strings('app/src/main/res/values/strings.xml', en_strings)
append_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

replacements = {
    r'"Trending Now"': 'stringResource(R.string.trending_now)',
    r'"متابعة المشاهدة"': 'stringResource(R.string.continue_watching)',
    r'"Trending Series"': 'stringResource(R.string.trending_series)',
    r'"Anime"': 'stringResource(R.string.anime)',
    r'"Coming Soon"': 'stringResource(R.string.coming_soon)',
    r'"New Releases"': 'stringResource(R.string.new_releases)',
    r'"Popular Series"': 'stringResource(R.string.popular_series)',
    r'"Popular Movies"': 'stringResource(R.string.popular_movies)',
    r'"Popular Anime"': 'stringResource(R.string.popular_anime)',
    r'"Popular Searches"': 'stringResource(R.string.popular_searches)',
    r'"Recent Searches"': 'stringResource(R.string.recent_searches)',
    r'"Clear All"': 'stringResource(R.string.clear_all)',
    r'"Edit >"': 'stringResource(R.string.edit_action)',
    r'"See All"': 'stringResource(R.string.see_all)'
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
