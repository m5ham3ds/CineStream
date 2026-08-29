package com.example.domain.providers

import com.example.source.AnimeSource
import com.example.source.ExampleAnimeSource
import com.example.source.Video
import com.example.source.Episode
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

data class Provider(
    val name: String,
    val type: ProviderType,
    val language: String,
    val logoUrl: String? = null
)

enum class ProviderType {
    ANIME, MOVIE, SERIES
}

data class VideoSource(
    val quality: String,
    val url: String, // Actual MP4/M3U8 link
    val providerName: String
)

object ProviderManager {
    // List of Aniyomi-style extensions (Sources)
    private val sources: List<AnimeSource> = listOf(
        ExampleAnimeSource()
        // Add your parsed HTTP sources here!
    )

    fun getActiveProviders(type: ProviderType): List<Provider> {
        return sources.map { source ->
            Provider(
                name = source.name,
                type = ProviderType.ANIME, // For demo
                language = source.lang
            )
        }
    }

    suspend fun extractVideoLinks(mediaId: String, isMovie: Boolean, episodeId: String? = null): List<VideoSource> = withContext(Dispatchers.IO) {
        val allVideos = mutableListOf<VideoSource>()
        
        // Loop through all sources to find video links
        for (source in sources) {
            try {
                // In a real scenario, you'd pass the actual Episode object that was parsed.
                // For this structure, we simulate passing an episode to get the video list.
                val dummyEpisode = Episode(url = "/episode/$episodeId")
                val videos = source.getVideoList(dummyEpisode)
                
                videos.forEach { video ->
                    if (video.videoUrl != null) {
                        allVideos.add(
                            VideoSource(
                                quality = video.quality,
                                url = video.videoUrl, // Real direct video URL
                                providerName = source.name
                            )
                        )
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        
        // If no sources are implemented yet, we return a real working MP4 for testing
        // to prove the ExoPlayer and Offline Download systems work.
        if (allVideos.isEmpty()) {
            allVideos.add(
                VideoSource(
                    quality = "720p (Test Video)",
                    url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                    providerName = "System"
                )
            )
        }
        
        return@withContext allVideos
    }
}
