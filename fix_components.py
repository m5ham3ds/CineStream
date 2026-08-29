import re

files = [
    'app/src/main/java/com/example/ui/components/HeroCarousel.kt',
    'app/src/main/java/com/example/ui/components/MediaCard.kt',
    'app/src/main/java/com/example/ui/components/SharedUI.kt'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Shared fix
    content = content.replace('Color(0xFF1E1E20)', 'MaterialTheme.colorScheme.surface')
    content = content.replace('Color(0xFF2A2A2E)', 'MaterialTheme.colorScheme.surfaceVariant')

    # Fix AlertDialog specific colors
    content = re.sub(r'title = \{ Text\("إزالة من المفضلة", color = Color.White\) \}', r'title = { Text("إزالة من المفضلة", color = MaterialTheme.colorScheme.onSurface) }', content)
    content = re.sub(r'text = \{ Text\("هل أنت متأكد أنك تريد إزالة هذا العمل من المفضلة؟", color = Color.LightGray\) \}', r'text = { Text("هل أنت متأكد أنك تريد إزالة هذا العمل من المفضلة؟", color = MaterialTheme.colorScheme.onSurfaceVariant) }', content)
    content = re.sub(r'Text\("إلغاء", color = Color.White\)', r'Text("إلغاء", color = MaterialTheme.colorScheme.onSurface)', content)

    # In SharedUI, the tags background is surface, text can be onSurface
    # actually, text on top of gradient in SharedUI should be Color.White.
    # Text(item.title, color = Color.White ... in SharedUI, if it's on top of gradient, white is good. But wait, in MediaItemRow, the background is Color(0xFF1E1E20) which is now surface. So the text should be onSurface.
    if 'SharedUI.kt' in filepath:
        # MediaItemRow
        content = content.replace('Text(item.title, color = Color.White', 'Text(item.title, color = MaterialTheme.colorScheme.onSurface')
        content = content.replace('Text(item.releaseDate, color = Color.Gray', 'Text(item.releaseDate, color = MaterialTheme.colorScheme.onSurfaceVariant')
        
    with open(filepath, 'w') as f:
        f.write(content)
