import re

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

get_old = """        } catch (e: Exception) {
            // Return a basic user object so the app doesn't think they are logged out,
            // but log the error.
            User(uid = firebaseUser.uid, email = firebaseUser.email ?: "", username = "user_" + firebaseUser.uid.take(5))
        }"""
get_new = """        } catch (e: Exception) {
            null
        }"""
content = content.replace(get_old, get_new)

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
