package com.example.domain.providers

data class VideoSource(
    val name: String,
    val url: String,
    val quality: String
)

interface VideoProvider {
    val name: String
    
    // Simulate scraping or API call to fetch video links for a specific movie or TV show.
    // In a real app, this would make network requests, parse HTML, extract m3u8/mp4 URLs, etc.
    suspend fun extractVideoLinks(mediaId: String, isMovie: Boolean): List<VideoSource>
}
