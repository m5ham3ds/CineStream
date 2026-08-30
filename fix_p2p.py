import re

filepath = 'app/src/main/java/com/example/utils/P2PManager.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Update sendMovie signature
send_movie_old = "fun sendMovie(endpointId: String, movieId: String, title: String, isMovie: Boolean, file: File)"
send_movie_new = "fun sendMovie(endpointId: String, movieId: String, title: String, isMovie: Boolean, posterUrl: String, file: File)"
content = content.replace(send_movie_old, send_movie_new)

metadata_old = """            metadata.put("title", title)
            metadata.put("isMovie", isMovie)"""
metadata_new = """            metadata.put("title", title)
            metadata.put("isMovie", isMovie)
            metadata.put("posterUrl", posterUrl)"""
content = content.replace(metadata_old, metadata_new)

# Update onMovieReceived signature
on_movie_received_old = "var onMovieReceived: ((String, String, Boolean) -> Unit)? = null"
on_movie_received_new = "var onMovieReceived: ((String, String, Boolean, String) -> Unit)? = null // id, title, isMovie, posterUrl"
content = content.replace(on_movie_received_old, on_movie_received_new)

# Update the parsing
parsing_old = """                    val id = incomingMetadata!!.getString("id")
                    val title = incomingMetadata!!.getString("title")
                    val isMovie = incomingMetadata!!.getBoolean("isMovie")
                    
                    // Rename file and move to correct directory
                    val destDir = File(context.filesDir, "downloads")
                    if (!destDir.exists()) destDir.mkdirs()
                    val destFile = File(destDir, "$id.mp4")
                    payloadFile.renameTo(destFile)
                    
                    onMovieReceived?.invoke(id, title, isMovie)"""
parsing_new = """                    val id = incomingMetadata!!.getString("id")
                    val title = incomingMetadata!!.getString("title")
                    val isMovie = incomingMetadata!!.getBoolean("isMovie")
                    val posterUrl = incomingMetadata!!.optString("posterUrl", "")
                    
                    // Rename file and move to correct directory
                    val destDir = File(context.filesDir, "downloads")
                    if (!destDir.exists()) destDir.mkdirs()
                    val destFile = File(destDir, "$id.mp4")
                    payloadFile.renameTo(destFile)
                    
                    onMovieReceived?.invoke(id, title, isMovie, posterUrl)"""
content = content.replace(parsing_old, parsing_new)

with open(filepath, 'w') as f:
    f.write(content)
