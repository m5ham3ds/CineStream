with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == '}':
        # Let's check if the previous line is @Composable
        if i > 0 and '@Composable' in lines[i-1]:
            continue # Skip it, we'll put it before @Composable
    new_lines.append(line)

# find @Composable before fun SettingsSectionHeader
target_idx = -1
for i, line in enumerate(new_lines):
    if 'fun SettingsSectionHeader' in line:
        target_idx = i - 1
        break

if target_idx != -1:
    new_lines.insert(target_idx, '}\n')

with open('app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt', 'w') as f:
    f.writelines(new_lines)
