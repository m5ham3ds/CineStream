import os
import glob

def fix_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Find the stray closing brace before `} else {`
    # It looks like:
    #     }
    #        
    #        } else {
    
    # Let's fix this reliably. The stray `}` belongs to the `Column`.
    # We should move it AFTER the `} else { ... }` block!
    
    # 1. We replace `\n    }\n        \n        } else {` with `\n        } else {`
    import re
    content = re.sub(r"    \}\s*\} else \{", "} else {", content)
    
    # 2. Add the `}` at the end of the `if/else` block, before `if (showBottomSheet) {`
    # The block ends with:
    #             }
    #         }
    # if (showBottomSheet) {
    # 
    # We should add `    }` to close the Column!
    
    content = content.replace("        }\nif (showBottomSheet) {", "        }\n    }\nif (showBottomSheet) {")
    
    with open(filepath, "w") as f:
        f.write(content)

fix_file("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt")
fix_file("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt")
fix_file("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt")
fix_file("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt")

