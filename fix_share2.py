import re

filepath = 'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

sig_old = """@Composable
fun ShareScreen(
    p2pManager: P2PManager,
    downloadRepository: DownloadRepository,
    onBack: () -> Unit
) {"""

sig_new = """@Composable
fun ShareScreen(
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val p2pManager = remember { P2PManager(context) }
    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }"""

content = content.replace(sig_old, sig_new)
content = content.replace('val context = LocalContext.current\n    val p2pState', 'val p2pState')
content = content.replace('val completedDownloads by downloadRepository.completedDownloads.collectAsState(initial = emptyList())', 'val completedDownloads by downloadRepository.getAllCompletedDownloads().collectAsState(initial = emptyList())')

with open(filepath, 'w') as f:
    f.write(content)
