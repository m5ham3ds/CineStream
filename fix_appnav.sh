#!/bin/bash
sed -i '460,467d' app/src/main/java/com/example/navigation/AppNavigation.kt

# Find Scaffold( and insert before it
sed -i '/Scaffold(/i \        if (isUpdatingData \&\& currentRoute != Screen.Splash.route \&\& currentRoute != Screen.Auth.route \&\& currentRoute != Screen.Onboarding.route) {\n            BackgroundWebView(\n                urls = extensionUrls,\n                onProgress = { },\n                onComplete = { isUpdatingData = false }\n            )\n        }' app/src/main/java/com/example/navigation/AppNavigation.kt
