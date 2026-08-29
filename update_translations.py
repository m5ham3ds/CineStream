import re
import os

# 1. Update strings.xml (English)
en_xml = 'app/src/main/res/values/strings.xml'
with open(en_xml, 'r') as f:
    en_content = f.read()

en_strings = """
    <string name="overview">Overview</string>
    <string name="cast">Cast</string>
    <string name="seasons_and_episodes">Seasons and Episodes</string>
    <string name="season_number">Season %1$d</string>
    <string name="premium_plan">Premium Plan</string>
    <string name="member_since">Member since May 2024</string>
    <string name="you_are_premium">You\'re Premium!</string>
    <string name="premium_desc">Enjoy ad-free streaming and exclusive content.</string>
    <string name="manage_plan">Manage Plan</string>
    <string name="account">Account</string>
    <string name="preferences">Preferences</string>
    <string name="edit">Edit</string>
    <string name="downloads_desc">Watch your content offline anytime, anywhere.</string>
    <string name="storage">Storage</string>
    <string name="download_more">Download more content</string>
    <string name="download_more_desc">Find movies and series to download and watch offline.</string>
    <string name="browse_content">Browse Content</string>
    <string name="email_hint">Email (Gmail)</string>
    <string name="password_hint">Password</string>
    <string name="remember_me">Remember me</string>
    <string name="or_continue_with">Or continue with</string>
    <string name="sign_in_with_google">Sign in with Google</string>
    <string name="sign_up">Sign Up</string>
    <string name="sign_in">Sign In</string>
    <string name="now_playing">Now Playing</string>
    <string name="episode_number">Episode %1$d</string>
    <string name="file_not_found">File not found on disk.</string>
    <string name="search_hint">Search movies &amp; series</string>
    <string name="cant_find">Can\'t find what you\'re looking for?</string>
    <string name="try_different_keyword">Try searching with a different keyword</string>
    <string name="explore_all_content">Explore All Content</string>
    <string name="select_episode">Select Episode</string>
    <string name="select_source">Select Source &amp; Quality</string>
    <string name="new_release">NEW RELEASE</string>
    <string name="play">Play</string>
    <string name="no_sources">No sources found.</string>
    <string name="add_to_library_favorites">Add to Library / Favorites</string>
    <string name="delete_download">Delete Download</string>
    <string name="delete_download_confirm">Are you sure you want to delete this item from downloads?</string>
    <string name="yes_delete">Yes, delete</string>
    <string name="cancel">Cancel</string>
    <string name="remove_from_favorites">Remove from Favorites</string>
    <string name="remove_from_favorites_confirm">Are you sure you want to remove this item from favorites?</string>
    <string name="remove">Remove</string>
    <string name="no_downloads_yet">You haven\'t downloaded anything yet</string>
    <string name="downloads_will_appear_here">Movies and series you download will appear here</string>
    <string name="search_dots">Search...</string>
    <string name="no_results">No results found</string>
    <string name="movie_singular">Movie</string>
    <string name="series_singular">Series</string>
</resources>
"""
if '<string name="overview">' not in en_content:
    en_content = en_content.replace('</resources>', en_strings.strip() + '\n</resources>')
    with open(en_xml, 'w') as f:
        f.write(en_content)

# 2. Update strings-ar.xml (Arabic)
ar_xml = 'app/src/main/res/values-ar/strings.xml'
with open(ar_xml, 'r') as f:
    ar_content = f.read()

ar_strings = """
    <string name="overview">نظرة عامة</string>
    <string name="cast">طاقم العمل</string>
    <string name="seasons_and_episodes">المواسم والحلقات</string>
    <string name="season_number">الموسم %1$d</string>
    <string name="premium_plan">الباقة المميزة</string>
    <string name="member_since">عضو منذ مايو 2024</string>
    <string name="you_are_premium">أنت في الباقة المميزة!</string>
    <string name="premium_desc">استمتع بمشاهدة بدون إعلانات ومحتوى حصري.</string>
    <string name="manage_plan">إدارة الباقة</string>
    <string name="account">الحساب</string>
    <string name="preferences">التفضيلات</string>
    <string name="edit">تعديل</string>
    <string name="downloads_desc">شاهد محتواك المفضل بدون إنترنت في أي وقت وفي أي مكان.</string>
    <string name="storage">مساحة التخزين</string>
    <string name="download_more">تنزيل المزيد من المحتوى</string>
    <string name="download_more_desc">ابحث عن أفلام ومسلسلات لتنزيلها ومشاهدتها بدون إنترنت.</string>
    <string name="browse_content">تصفح المحتوى</string>
    <string name="email_hint">البريد الإلكتروني (Gmail)</string>
    <string name="password_hint">كلمة المرور</string>
    <string name="remember_me">تذكرني</string>
    <string name="or_continue_with">أو المتابعة باستخدام</string>
    <string name="sign_in_with_google">تسجيل الدخول بحساب جوجل</string>
    <string name="sign_up">إنشاء حساب</string>
    <string name="sign_in">تسجيل الدخول</string>
    <string name="now_playing">يعرض الآن</string>
    <string name="episode_number">الحلقة %1$d</string>
    <string name="file_not_found">الملف غير موجود على الجهاز.</string>
    <string name="search_hint">ابحث عن أفلام ومسلسلات</string>
    <string name="cant_find">لم تجد ما تبحث عنه؟</string>
    <string name="try_different_keyword">جرب البحث بكلمة مفتاحية أخرى</string>
    <string name="explore_all_content">استكشف كل المحتوى</string>
    <string name="select_episode">اختر الحلقة</string>
    <string name="select_source">اختر المصدر والجودة</string>
    <string name="new_release">إصدار جديد</string>
    <string name="play">تشغيل</string>
    <string name="no_sources">لم يتم العثور على مصادر.</string>
    <string name="add_to_library_favorites">إضافة للمكتبة / المفضلة</string>
    <string name="delete_download">حذف التنزيل</string>
    <string name="delete_download_confirm">هل أنت متأكد أنك تريد حذف هذا العنصر من التنزيلات؟</string>
    <string name="yes_delete">نعم، احذف</string>
    <string name="cancel">إلغاء</string>
    <string name="remove_from_favorites">إزالة من المفضلة</string>
    <string name="remove_from_favorites_confirm">هل أنت متأكد أنك تريد إزالة هذا العمل من المفضلة؟</string>
    <string name="remove">إزالة</string>
    <string name="no_downloads_yet">لم تقم بتنزيل أي عمل بعد</string>
    <string name="downloads_will_appear_here">الأفلام والمسلسلات التي تنزلها ستظهر هنا</string>
    <string name="search_dots">البحث...</string>
    <string name="no_results">لا توجد نتائج</string>
    <string name="movie_singular">فيلم</string>
    <string name="series_singular">مسلسل</string>
</resources>
"""
if '<string name="overview">' not in ar_content:
    ar_content = ar_content.replace('</resources>', ar_strings.strip() + '\n</resources>')
    with open(ar_xml, 'w') as f:
        f.write(ar_content)
