import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# Replace the BackgroundWebView definition
content = re.sub(
    r"        if \(isUpdatingData && currentRoute != Screen\.Splash\.route && currentRoute != Screen\.Auth\.route && currentRoute != Screen\.Onboarding\.route\) \{\s*BackgroundWebView\(\s*urls = extensionUrls,\s*onProgress = \{ \},\s*onComplete = \{ isUpdatingData = false \}\s*\)\s*\}",
    """        if (isUpdatingData && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route && !updateFinishedShowGreen) {
            SiteVerificationManager.isVerificationStarted = true
            BackgroundWebView(
                urls = extensionUrls,
                onProgress = { },
                onSiteVerified = { url -> SiteVerificationManager.markSiteVerified(url) },
                onComplete = { 
                    SiteVerificationManager.isVerificationComplete = true
                    updateFinishedShowGreen = true 
                }
            )
        }""",
    content
)

# Now remove the old Box above topbar
content = re.sub(
    r"                    if \(isUpdatingData && currentRoute != Screen\.Splash\.route && currentRoute != Screen\.Auth\.route && currentRoute != Screen\.Onboarding\.route\) \{\s*Box\(\s*modifier = Modifier\s*\.fillMaxWidth\(\)\s*\.background\(Color\(0xFF2C2C2E\)\)\s*\.padding\(vertical = 4\.dp\),\s*contentAlignment = Alignment\.Center\s*\) \{\s*Text\(\s*text = stringResource\(R\.string\.updating_data\),\s*color = Color\.White,\s*fontSize = 12\.sp\s*\)\s*\}\s*\}",
    "",
    content
)

# Insert the new Box below the topbar content
# We'll find the CenterAlignedTopAppBar block end, or just add it at the end of the topBar Column.
# The topBar Column starts at `topBar = {\n                Column {`
# We can find `                        }\n                    }\n                }\n            },` which is the end of topBar.
# Actually, the easiest way is to look for the end of the topBar block:
# It's `                    }\n                }\n            },` (end of if bottomBarRoutes... Column and the outer Column).
# Let's insert the new Box right before the closing `}` of the outer `Column {` of `topBar = {`.
content = content.replace(
    """                    }
                }
            },""",
    """                    }
                    if ((isUpdatingData || updateFinishedShowGreen) && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(if (updateFinishedShowGreen) Color(0xFF4CAF50) else primaryColorVal)
                                .padding(vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = if (updateFinishedShowGreen) "تم التحقق من جميع المواقع بنجاح" else stringResource(R.string.updating_data),
                                color = Color.White,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            },"""
)


with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
