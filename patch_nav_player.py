import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Update MovieDetailsScreen onPlay
movie_target = """onPlay = { url -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                navController.navigate("player?url=$encodedUrl")
                            }
                        }"""
movie_replacement = """onPlay = { title, url -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?url=$encodedUrl&title=$encodedTitle")
                            }
                        }"""
content = content.replace(movie_target, movie_replacement)

# Update SeriesDetailsScreen onPlay
series_target = """onPlay = { url -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                navController.navigate("player?url=$encodedUrl")
                            }
                        }"""
series_replacement = """onPlay = { title, url -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?url=$encodedUrl&title=$encodedTitle")
                            }
                        }"""
content = content.replace(series_target, series_replacement)

# Update PlayerScreen route
player_route_target = """composable("player?url={url}") { backStackEntry ->
                    val url = backStackEntry.arguments?.getString("url") ?: return@composable
                    val decodedUrl = URLDecoder.decode(url, "UTF-8")
                    PlayerScreen(videoUrl = decodedUrl, onBack = { navController.popBackStack() })
                }"""
player_route_replacement = """composable("player?url={url}&title={title}") { backStackEntry ->
                    val url = backStackEntry.arguments?.getString("url") ?: return@composable
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val decodedUrl = URLDecoder.decode(url, "UTF-8")
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    PlayerScreen(videoUrl = decodedUrl, title = decodedTitle, onBack = { navController.popBackStack() })
                }"""
content = content.replace(player_route_target, player_route_replacement)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
