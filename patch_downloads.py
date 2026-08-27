import re

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    content = f.read()

demo_card_pattern = r"        // Download Item Card.*?        // Storage Card"
demo_card_match = re.search(demo_card_pattern, content, flags=re.DOTALL)

empty_state = """        // Empty State
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 48.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(Icons.Outlined.Download, contentDescription = null, tint = Color.DarkGray, modifier = Modifier.size(64.dp))
            Spacer(modifier = Modifier.height(16.dp))
            Text("لم تقم بتنزيل أي عمل بعد", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))
            Text("الأفلام والمسلسلات التي تنزلها ستظهر هنا", color = Color.Gray, fontSize = 14.sp)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        // Storage Card"""

if demo_card_match:
    content = content.replace(demo_card_match.group(0), empty_state)

# Replace values in the Stats row to be zeros since empty
content = content.replace('value = "1", label = "Downloaded"', 'value = "0", label = "Downloaded"')
content = content.replace('value = "1", label = "Completed"', 'value = "0", label = "Completed"')

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(content)

