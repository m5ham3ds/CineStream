import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

# I will replace the AlertDialog content for Send Dialog.
old_dialog = """    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = {
                showSendDialog = false
                p2pManager.stopAll()
            },
            title = { Text("Select Media to Send", fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    if (p2pState == P2PState.DISCOVERING && discoveredEndpoints.isEmpty()) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(16.dp))
                        Text("Looking for devices...", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                    } else if (discoveredEndpoints.isNotEmpty() && connectedEndpoint == null) {
                        Text("Available Devices:", fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 8.dp))
                        discoveredEndpoints.forEach { endpoint ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { p2pManager.requestConnection(endpoint.id, Build.MODEL) }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.PhoneAndroid, contentDescription = null)
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(endpoint.name)
                            }
                        }
                    } else if (connectedEndpoint != null) {
                        Text("Connected to ${connectedEndpoint?.name}", color = Color.Green, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                            if (completedDownloads.isEmpty()) {
                                item { Text("No downloaded movies found.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                            }
                            
                            // Group by Type
                            val movies = completedDownloads.filter { it.isMovie }
                            val series = completedDownloads.filter { !it.isMovie }
                            
                            if (movies.isNotEmpty()) {
                                item { Text("Movies", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                items(movies) { item ->
                                    SendItemRow(item, context, p2pManager, connectedEndpoint) { showSendDialog = false }
                                }
                            }
                            
                            if (series.isNotEmpty()) {
                                item { Text("Series / Anime", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                items(series) { item ->
                                    SendItemRow(item, context, p2pManager, connectedEndpoint) { showSendDialog = false }
                                }
                            }
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showSendDialog = false
                    p2pManager.stopAll()
                }) { Text("Cancel") }
            }
        )
    }"""

new_dialog = """    var selectedFolder by remember { mutableStateOf<String?>(null) }
    
    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = {
                showSendDialog = false
                selectedFolder = null
                p2pManager.stopAll()
            },
            title = { Text(if (selectedFolder == null) "Select Media to Send" else selectedFolder!!, fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    if (p2pState == P2PState.DISCOVERING && discoveredEndpoints.isEmpty()) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(16.dp))
                        Text("Looking for devices...", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                    } else if (discoveredEndpoints.isNotEmpty() && connectedEndpoint == null) {
                        Text("Available Devices:", fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 8.dp))
                        discoveredEndpoints.forEach { endpoint ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { p2pManager.requestConnection(endpoint.id, Build.MODEL) }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.PhoneAndroid, contentDescription = null)
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(endpoint.name)
                            }
                        }
                    } else if (connectedEndpoint != null) {
                        Text("Connected to ${connectedEndpoint?.name}", color = Color.Green, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                            if (completedDownloads.isEmpty()) {
                                item { Text("No downloaded movies found.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                            } else {
                                if (selectedFolder == null) {
                                    // Group by Type/Title
                                    val movies = completedDownloads.filter { it.isMovie }
                                    val series = completedDownloads.filter { !it.isMovie }
                                    
                                    if (movies.isNotEmpty()) {
                                        item { Text("Movies", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        items(movies) { item ->
                                            SendItemRow(item, context, p2pManager, connectedEndpoint) { 
                                                showSendDialog = false 
                                                selectedFolder = null
                                            }
                                        }
                                    }
                                    
                                    if (series.isNotEmpty()) {
                                        item { Text("Series / Anime", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        
                                        // Group series by title (creating folders)
                                        val groupedSeries = series.groupBy { it.title.split(" - ").firstOrNull() ?: it.title }
                                        
                                        items(groupedSeries.keys.toList()) { folderName ->
                                            Row(
                                                modifier = Modifier
                                                    .fillMaxWidth()
                                                    .clickable { selectedFolder = folderName }
                                                    .padding(vertical = 12.dp, horizontal = 8.dp),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Icon(Icons.Outlined.Folder, contentDescription = "Folder", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                                                Spacer(modifier = Modifier.width(16.dp))
                                                Column(modifier = Modifier.weight(1f)) {
                                                    Text(folderName, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                                    Text("${groupedSeries[folderName]?.size ?: 0} Episodes", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                                                }
                                                Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Open", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                            }
                                        }
                                    }
                                } else {
                                    // Inside a folder
                                    item {
                                        Row(
                                            modifier = Modifier.fillMaxWidth().clickable { selectedFolder = null }.padding(vertical = 8.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.primary)
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Text("Back to Folders", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                    
                                    val folderItems = completedDownloads.filter { !it.isMovie && (it.title.split(" - ").firstOrNull() ?: it.title) == selectedFolder }
                                    items(folderItems) { item ->
                                        SendItemRow(item, context, p2pManager, connectedEndpoint) { 
                                            showSendDialog = false 
                                            selectedFolder = null
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showSendDialog = false
                    selectedFolder = null
                    p2pManager.stopAll()
                }) { Text("Cancel") }
            }
        )
    }"""

content = content.replace(old_dialog, new_dialog)

with open(filepath, 'w') as f:
    f.write(content)
