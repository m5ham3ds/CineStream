import re
import os

en_strings = """
    <string name="about_mission_desc">To deliver the best entertainment experience with a simple, fast and beautiful streaming platform.</string>
    <string name="feature_reliable_title">Reliable</string>
    <string name="feature_reliable_desc">Secure and stable streaming experience.</string>
    <string name="feature_fast_title">Fast</string>
    <string name="feature_fast_desc">Optimized performance for everyone.</string>
    <string name="feature_premium_title">Premium</string>
    <string name="feature_premium_desc">High quality content and features.</string>
    <string name="feature_made_for_you_title">Made for You</string>
    <string name="feature_made_for_you_desc">Designed to bring you the best.</string>
    <string name="link_meet_team">Meet the Team</string>
    <string name="link_terms">Terms of Service</string>
    <string name="link_privacy">Privacy Policy</string>
    <string name="link_contact">Contact Us</string>
"""

ar_strings = """
    <string name="about_mission_desc">تقديم أفضل تجربة ترفيهية من خلال منصة بث بسيطة وسريعة وجميلة.</string>
    <string name="feature_reliable_title">موثوقية</string>
    <string name="feature_reliable_desc">تجربة بث آمنة ومستقرة.</string>
    <string name="feature_fast_title">سرعة</string>
    <string name="feature_fast_desc">أداء مُحسّن للجميع.</string>
    <string name="feature_premium_title">مميز</string>
    <string name="feature_premium_desc">محتوى وميزات عالية الجودة.</string>
    <string name="feature_made_for_you_title">صُنع من أجلك</string>
    <string name="feature_made_for_you_desc">مُصمم ليقدم لك الأفضل.</string>
    <string name="link_meet_team">فريق العمل</string>
    <string name="link_terms">شروط الخدمة</string>
    <string name="link_privacy">سياسة الخصوصية</string>
    <string name="link_contact">اتصل بنا</string>
"""

def append_strings(file, new_strings):
    with open(file, 'r') as f:
        content = f.read()
    if '<string name="link_meet_team">' not in content:
        content = content.replace('</resources>', new_strings.strip() + '\n</resources>')
        with open(file, 'w') as f:
            f.write(content)

append_strings('app/src/main/res/values/strings.xml', en_strings)
append_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

filepath = 'app/src/main/java/com/example/ui/screens/about/AboutScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    '"To deliver the best entertainment experience with a simple, fast and beautiful streaming platform."',
    'stringResource(R.string.about_mission_desc)'
)
content = content.replace(
    'title = "Reliable", subtitle = "Secure and stable streaming experience."',
    'title = stringResource(R.string.feature_reliable_title), subtitle = stringResource(R.string.feature_reliable_desc)'
)
content = content.replace(
    'title = "Fast", subtitle = "Optimized performance for everyone."',
    'title = stringResource(R.string.feature_fast_title), subtitle = stringResource(R.string.feature_fast_desc)'
)
content = content.replace(
    'title = "Premium", subtitle = "High quality content and features."',
    'title = stringResource(R.string.feature_premium_title), subtitle = stringResource(R.string.feature_premium_desc)'
)
content = content.replace(
    'title = "Made for You", subtitle = "Designed to bring you the best."',
    'title = stringResource(R.string.feature_made_for_you_title), subtitle = stringResource(R.string.feature_made_for_you_desc)'
)
content = content.replace(
    'title = "Meet the Team"',
    'title = stringResource(R.string.link_meet_team)'
)
content = content.replace(
    'title = "Terms of Service"',
    'title = stringResource(R.string.link_terms)'
)
content = content.replace(
    'title = "Privacy Policy"',
    'title = stringResource(R.string.link_privacy)'
)
content = content.replace(
    'title = "Contact Us"',
    'title = stringResource(R.string.link_contact)'
)

with open(filepath, 'w') as f:
    f.write(content)

