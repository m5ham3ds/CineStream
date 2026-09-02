import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

chat_route_old = """            composable("chat/{conversationId}") { backStackEntry ->
                val convId = backStackEntry.arguments?.getString("conversationId") ?: return@composable
                ChatScreen(
                    conversationId = convId,
                    onBack = { navController.popBackStack() }
                )
            }"""

chat_route_new = """            composable("chat/{conversationId}") { backStackEntry ->
                val convId = backStackEntry.arguments?.getString("conversationId") ?: return@composable
                ChatScreen(
                    conversationId = convId,
                    onBack = { navController.popBackStack() },
                    onUserClick = { userId ->
                        navController.navigate(Screen.PublicProfile.createRoute(userId))
                    }
                )
            }"""

content = content.replace(chat_route_old, chat_route_new)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

