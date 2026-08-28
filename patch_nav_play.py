with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace(
    """onPlay = { url -> 
                            val encodedUrl = URLEncoder.encode(url, "UTF-8")
                            navController.navigate("player?url=$encodedUrl")
                        }""",
    """onPlay = { url -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                navController.navigate("player?url=$encodedUrl")
                            }
                        }"""
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
