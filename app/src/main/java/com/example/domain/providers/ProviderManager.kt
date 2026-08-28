package com.example.domain.providers

import kotlinx.coroutines.delay

// This acts like the "Extensions" manager, but integrated directly into the app.
object ProviderManager {
    val providers: List<VideoProvider> = listOf(
        ServerOneProvider(),
        ServerTwoProvider(),
        ServerThreeProvider()
    )

    suspend fun fetchAllSources(mediaId: String, isMovie: Boolean): List<Pair<String, VideoSource>> {
        val results = mutableListOf<Pair<String, VideoSource>>()
        // Fetch from all integrated providers concurrently or sequentially
        for (provider in providers) {
            try {
                val sources = provider.extractVideoLinks(mediaId, isMovie)
                sources.forEach { source ->
                    results.add(Pair(provider.name, source))
                }
            } catch (e: Exception) {
                // Ignore failure for a specific provider
            }
        }
        return results
    }
}

class ServerOneProvider : VideoProvider {
    override val name: String = "Server 1 (Fast)"

    override suspend fun extractVideoLinks(mediaId: String, isMovie: Boolean): List<VideoSource> {
        delay(800) // Simulate network request scraping
        return listOf(
            VideoSource("Main Stream", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "1080p"),
            VideoSource("Backup Stream", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "720p")
        )
    }
}

class ServerTwoProvider : VideoProvider {
    override val name: String = "Server 2 (Multi-Sub)"

    override suspend fun extractVideoLinks(mediaId: String, isMovie: Boolean): List<VideoSource> {
        delay(1200) // Simulate network request scraping
        return listOf(
            VideoSource("Direct Mp4", "https://html5demos.com/assets/dizzy.mp4", "720p")
        )
    }
}

class ServerThreeProvider : VideoProvider {
    override val name: String = "Server 3 (VIP)"

    override suspend fun extractVideoLinks(mediaId: String, isMovie: Boolean): List<VideoSource> {
        delay(500) // Simulate network request scraping
        return listOf(
            VideoSource("HLS Stream", "https://devstreaming-cdn.apple.com/videos/streaming/examples/img_bipbop_adv_example_fmp4/master.m3u8", "4K")
        )
    }
}
