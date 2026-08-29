import re

with open('app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt', 'r') as f:
    lines = f.readlines()

# Remove line 170 (index 169) which is the extra '}'
if lines[169].strip() == '}':
    lines.pop(169)
    print("Removed extra '}' at line 170")
    
    # We need to add a '}' after the if/else block to close the Column
    # Let's find 'if (showBottomSheet)'
    for i, line in enumerate(lines):
        if 'if (showBottomSheet)' in line:
            lines.insert(i, '    }\n')
            print(f"Added '}}' at line {i+1} to close Column")
            break

with open('app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt', 'w') as f:
    f.writelines(lines)
