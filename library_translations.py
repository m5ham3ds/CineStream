import re
import os

en_strings = """
    <string name="library">Library</string>
    <string name="watchlist">Watchlist</string>
    <string name="downloads">Downloads</string>
    <string name="history">History</string>
    <string name="empty_watchlist">Your watchlist is empty</string>
    <string name="empty_downloads">Your downloads are empty</string>
    <string name="empty_history">Your history is empty</string>
"""

ar_strings = """
    <string name="library">المكتبة</string>
    <string name="watchlist">قائمة المشاهدة</string>
    <string name="downloads">التنزيلات</string>
    <string name="history">السجل</string>
    <string name="empty_watchlist">قائمة المشاهدة فارغة</string>
    <string name="empty_downloads">التنزيلات فارغة</string>
    <string name="empty_history">السجل فارغ</string>
"""

def append_strings(file, new_strings):
    with open(file, 'r') as f:
        content = f.read()
    if '<string name="watchlist">' not in content:
        content = content.replace('</resources>', new_strings.strip() + '\n</resources>')
        with open(file, 'w') as f:
            f.write(content)

append_strings('app/src/main/res/values/strings.xml', en_strings)
append_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

filepath = 'app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    'TabItem("Watchlist", Icons.Default.Favorite)',
    'TabItem(stringResource(R.string.watchlist), Icons.Default.Favorite)'
)
content = content.replace(
    'TabItem("Downloads", Icons.Default.Download)',
    'TabItem(stringResource(R.string.downloads), Icons.Default.Download)'
)
content = content.replace(
    'TabItem("History", Icons.Default.History)',
    'TabItem(stringResource(R.string.history), Icons.Default.History)'
)
content = content.replace(
    'var selectedTab by remember { mutableStateOf("Watchlist") }',
    'val watchlistStr = stringResource(R.string.watchlist)\n    val downloadsStr = stringResource(R.string.downloads)\n    var selectedTab by remember { mutableStateOf(watchlistStr) }'
)
content = content.replace('selectedTab == "Watchlist"', 'selectedTab == watchlistStr')
content = content.replace('selectedTab == "Downloads"', 'selectedTab == downloadsStr')
content = content.replace('text = "Library"', 'text = stringResource(R.string.library)')
content = content.replace(
    'text = "Your ${selectedTab.lowercase()} is empty"',
    'text = if (selectedTab == watchlistStr) stringResource(R.string.empty_watchlist) else if (selectedTab == downloadsStr) stringResource(R.string.empty_downloads) else stringResource(R.string.empty_history)'
)

if 'import androidx.compose.ui.res.stringResource' not in content:
    content = content.replace('import androidx.compose.ui.unit.sp', 'import androidx.compose.ui.unit.sp\nimport androidx.compose.ui.res.stringResource\nimport com.example.R')

with open(filepath, 'w') as f:
    f.write(content)

