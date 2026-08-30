import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Remove topBar
top_bar_pattern = r"        topBar = \{\s*TopAppBar\(\s*title = \{ Text\(\"Offline Share\", fontWeight = FontWeight\.Bold\) \},\s*navigationIcon = \{\s*IconButton\(onClick = onBack\) \{ Icon\(Icons\.AutoMirrored\.Filled\.ArrowBack, contentDescription = \"Back\"\) \}\s*\},\s*colors = TopAppBarDefaults\.topAppBarColors\(containerColor = MaterialTheme\.colorScheme\.background\)\s*\)\s*\},"
content = re.sub(top_bar_pattern, "", content, flags=re.DOTALL)

# Remove the permission block
permissions_block_pattern = r"        if \(!permissionsState\.allPermissionsGranted\) \{.*?\s*return@Scaffold\s*\}"
content = re.sub(permissions_block_pattern, "", content, flags=re.DOTALL)

# Update clicks
send_click = r"modifier = Modifier\.weight\(1f\)\.clickable \{ p2pManager\.startDiscovery\(\) \},"
new_send_click = "modifier = Modifier.weight(1f).clickable { if (permissionsState.allPermissionsGranted) { p2pManager.startDiscovery() } else { permissionsState.launchMultiplePermissionRequest() } },"
content = content.replace(send_click, new_send_click)

receive_click = r"modifier = Modifier\.weight\(1f\)\.clickable \{ p2pManager\.startAdvertising\(android\.os\.Build\.MODEL\) \},"
new_receive_click = "modifier = Modifier.weight(1f).clickable { if (permissionsState.allPermissionsGranted) { p2pManager.startAdvertising(android.os.Build.MODEL) } else { permissionsState.launchMultiplePermissionRequest() } },"
content = content.replace(receive_click, new_receive_click)

scan_click = r"Row\(verticalAlignment = Alignment\.CenterVertically, modifier = Modifier\.clickable \{ p2pManager\.startDiscovery\(\) \}\) \{"
new_scan_click = "Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { if (permissionsState.allPermissionsGranted) { p2pManager.startDiscovery() } else { permissionsState.launchMultiplePermissionRequest() } }) {"
content = content.replace(scan_click, new_scan_click)

with open(filepath, 'w') as f:
    f.write(content)
