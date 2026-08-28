import re

for filepath in ["app/src/main/java/com/example/ui/screens/home/PopularScreen.kt", 
                 "app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt", 
                 "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt"]:
    with open(filepath, "r") as f:
        content = f.read()

    # I accidentally added "}\n}\n}" at the end of the file in the previous script by replacing "}\n}\n}" with "}\n}\n}\n}".
    # Wait, the previous script replaced "        }\n    }\n}" with "        }\n    }\n}\n}".
    # I should just run `git checkout` to restore them, and do it properly.

