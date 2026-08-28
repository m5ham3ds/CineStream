import re
import os

files = [
    "app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/PopularScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt"
]

for file in files:
    if not os.path.exists(file): continue
    with open(file, "r") as f:
        content = f.read()

    # Find where LazyVerticalGrid ends. It ends at the third closing brace from the end of the file.
    # We can just replace:
    #                 }
    #             }
    #         }
    #     }
    # }
    
    # Or just replace the entire block using regex
    pattern = r"(LazyVerticalGrid\([\s\S]*?\)\s*\{\s*itemsIndexed\(items\) \{[\s\S]*?\}\s*\})"
    match = re.search(pattern, content)
    if match:
        grid_code = match.group(1)
        content = content.replace(grid_code, grid_code + "\n            }")
        
    with open(file, "w") as f:
        f.write(content)

