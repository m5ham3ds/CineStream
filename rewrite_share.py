import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove TopAppBar
top_bar_pattern = r"topBar = \{\s*TopAppBar\(.*?colors = TopAppBarDefaults\.topAppBarColors\(containerColor = MaterialTheme\.colorScheme\.background\)\s*\)\s*\},"
content = re.sub(top_bar_pattern, "", content, flags=re.DOTALL)

# 2. Fix the padding in Scaffold content and remove the if (!permissionsState.allPermissionsGranted) block
permissions_block_pattern = r"if \(!permissionsState\.allPermissionsGranted\) \{.*?\s*return@Scaffold\s*\}"
content = re.sub(permissions_block_pattern, "", content, flags=re.DOTALL)

# 3. Update the button clicks for Send/Receive to request permissions if not granted
# Currently: onClick = { p2pManager.startDiscovering() }
# Replace with: onClick = { if (permissionsState.allPermissionsGranted) p2pManager.startDiscovering() else permissionsState.launchMultiplePermissionRequest() }

# Wait, let's find the exact onClick handlers in ShareScreen.kt
