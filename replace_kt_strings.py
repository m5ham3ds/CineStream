import re
import os

replacements = {
    r'Text\("Overview"': 'Text(stringResource(R.string.overview)',
    r'Text\("Cast"': 'Text(stringResource(R.string.cast)',
    r'Text\("Seasons and Episodes"': 'Text(stringResource(R.string.seasons_and_episodes)',
    r'Text\("Season \$\{season\.seasonNumber\}"': 'Text(stringResource(R.string.season_number, season.seasonNumber)',
    r'Text\("Premium Plan"': 'Text(stringResource(R.string.premium_plan)',
    r'Text\("Member since May 2024"': 'Text(stringResource(R.string.member_since)',
    r'Text\("You\'re Premium!"': 'Text(stringResource(R.string.you_are_premium)',
    r'Text\("Enjoy ad-free streaming and exclusive content."': 'Text(stringResource(R.string.premium_desc)',
    r'Text\("Manage Plan"': 'Text(stringResource(R.string.manage_plan)',
    r'Text\("Account"': 'Text(stringResource(R.string.account)',
    r'Text\("Preferences"': 'Text(stringResource(R.string.preferences)',
    
    r'Text\("Downloads"': 'Text(stringResource(R.string.downloads)',
    r'Text\("Edit"': 'Text(stringResource(R.string.edit)',
    r'Text\("Watch your content offline anytime, anywhere."': 'Text(stringResource(R.string.downloads_desc)',
    r'Text\("Storage"': 'Text(stringResource(R.string.storage)',
    r'Text\("Download more content"': 'Text(stringResource(R.string.download_more)',
    r'Text\("Find movies and series to download and watch offline."': 'Text(stringResource(R.string.download_more_desc)',
    r'Text\("Browse Content"': 'Text(stringResource(R.string.browse_content)',
    
    r'Text\("Email \(Gmail\)"': 'Text(stringResource(R.string.email_hint)',
    r'Text\("Password"': 'Text(stringResource(R.string.password_hint)',
    r'Text\("Remember me"': 'Text(stringResource(R.string.remember_me)',
    r'Text\("Or continue with"': 'Text(stringResource(R.string.or_continue_with)',
    r'Text\("Sign in with Google"': 'Text(stringResource(R.string.sign_in_with_google)',
    r'Text\(if \(isSignUp\) "Sign Up" else "Sign In"': 'Text(if (isSignUp) stringResource(R.string.sign_up) else stringResource(R.string.sign_in)',
    
    r'Text\("Now Playing"': 'Text(stringResource(R.string.now_playing)',
    r'Text\("Episode 1"': 'Text(stringResource(R.string.episode_number, 1)',
    r'Text\("File not found on disk."': 'Text(stringResource(R.string.file_not_found)',
    
    r'Text\("Search movies & series"': 'Text(stringResource(R.string.search_hint)',
    r'Text\("Can\'t find what you\'re looking for\?"': 'Text(stringResource(R.string.cant_find)',
    r'Text\("Try searching with a different keyword"': 'Text(stringResource(R.string.try_different_keyword)',
    r'Text\("Explore All Content"': 'Text(stringResource(R.string.explore_all_content)',
    
    r'Text\("Select Episode"': 'Text(stringResource(R.string.select_episode)',
    r'Text\("Select Source & Quality"': 'Text(stringResource(R.string.select_source)',
    r'Text\("NEW RELEASE"': 'Text(stringResource(R.string.new_release)',
    r'Text\("Play"': 'Text(stringResource(R.string.play)',
    r'Text\("No sources found."': 'Text(stringResource(R.string.no_sources)',
    r'Text\(text = "Add to Library / Favorites"': 'Text(text = stringResource(R.string.add_to_library_favorites)',
    r'Text\(text = "Episode \$ep"': 'Text(text = stringResource(R.string.episode_number, ep)',

    r'Text\("حذف التنزيل"': 'Text(stringResource(R.string.delete_download)',
    r'Text\("هل أنت متأكد أنك تريد حذف هذا العنصر من التنزيلات\؟"': 'Text(stringResource(R.string.delete_download_confirm)',
    r'Text\("نعم، احذف"': 'Text(stringResource(R.string.yes_delete)',
    r'Text\("إلغاء"': 'Text(stringResource(R.string.cancel)',
    r'Text\("إزالة من المفضلة"': 'Text(stringResource(R.string.remove_from_favorites)',
    r'Text\("هل أنت متأكد أنك تريد إزالة هذا العمل من المفضلة\؟"': 'Text(stringResource(R.string.remove_from_favorites_confirm)',
    r'Text\("إزالة"': 'Text(stringResource(R.string.remove)',
    r'Text\("لم تقم بتنزيل أي عمل بعد"': 'Text(stringResource(R.string.no_downloads_yet)',
    r'Text\("الأفلام والمسلسلات التي تنزلها ستظهر هنا"': 'Text(stringResource(R.string.downloads_will_appear_here)',
    r'Text\("البحث\.\.\."': 'Text(stringResource(R.string.search_dots)',
    r'Text\("لا توجد نتائج"': 'Text(stringResource(R.string.no_results)',
    r'Text\("\$year • \$\{if\(isMovie\) "فيلم" else "مسلسل"\}\"': 'Text("$year • ${if(isMovie) stringResource(R.string.movie_singular) else stringResource(R.string.series_singular)}"',
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

