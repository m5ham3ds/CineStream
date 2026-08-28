for filepath in ["app/src/main/java/com/example/ui/screens/home/PopularScreen.kt", 
                 "app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt", 
                 "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt"]:
    with open(filepath, "r") as f:
        content = f.read()

    # Revert the closing brace we added
    if filepath != "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt":
        # Popular and NewReleases had LazyVerticalGrid matched, so they actually needed ONE extra brace at the end of the PullToRefreshBox,
        # but my script replaced the end of the file braces incorrectly.
        
        # Let's fix the end of file braces.
        while content.endswith("}\n}"):
            content = content[:-2]
        content = content.strip() + "\n"
        
        # We need to make sure the PullToRefreshBox is closed correctly.
        # But wait, it's easier to just count the braces and add what's missing or remove extras.
        # Actually, let's just do a simple brace counter.
        brace_count = 0
        for char in content:
            if char == '{': brace_count += 1
            if char == '}': brace_count -= 1
        
        if brace_count > 0:
            content += "}\n" * brace_count
        elif brace_count < 0:
            # We have too many closing braces
            # Remove from the end
            for _ in range(-brace_count):
                content = content.rstrip()
                if content.endswith('}'):
                    content = content[:-1]
    else:
        # WatchingScreen did not have LazyVerticalGrid, so it just got extra braces at the end.
        while content.endswith("}\n}"):
            content = content[:-2]
        content = content.strip() + "\n"
        
        brace_count = 0
        for char in content:
            if char == '{': brace_count += 1
            if char == '}': brace_count -= 1
        
        if brace_count > 0:
            content += "}\n" * brace_count
        elif brace_count < 0:
            for _ in range(-brace_count):
                content = content.rstrip()
                if content.endswith('}'):
                    content = content[:-1]

    with open(filepath, "w") as f:
        f.write(content)
