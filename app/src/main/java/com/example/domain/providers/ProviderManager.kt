package com.example.domain.providers

import com.example.domain.provider.ServerAggregator
import com.example.domain.provider.ContentProvider
import com.example.domain.models.VideoStream
import com.example.domain.models.VideoQuality
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

// Central point for the UI to get aggregated streams
object ProviderManager {
    val aggregator = ServerAggregator().apply {
        // Here you will register your actual ContentProviders from your SERVER-OF-CONTENT repo
        registerProvider(MockServerOne())
        registerProvider(MockServerTwo())
    }
}

// Sample ContentProvider mimicking the structure of SERVER-OF-CONTENT
class MockServerOne : ContentProvider {
    override val name = "VidSrc (Server 1)"

    override suspend fun getMovieStreams(
        title: String,
        originalTitle: String,
        year: Int,
        tmdbId: String
    ): Flow<List<VideoStream>> = flow {
        delay(800) // Simulate network delay
        emit(listOf(
            VideoStream(name, VideoQuality.Q_1080, "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"),
            VideoStream(name, VideoQuality.Q_720, "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        ))
    }

    override suspend fun getEpisodeStreams(
        title: String,
        originalTitle: String,
        season: Int,
        episode: Int
    ): Flow<List<VideoStream>> = flow {
        delay(800)
        emit(listOf(
            VideoStream(name, VideoQuality.Q_1080, "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        ))
    }
}

class MockServerTwo : ContentProvider {
    override val name = "SuperStream (Server 2)"

    override suspend fun getMovieStreams(
        title: String,
        originalTitle: String,
        year: Int,
        tmdbId: String
    ): Flow<List<VideoStream>> = flow {
        delay(1200)
        emit(listOf(
            VideoStream(name, VideoQuality.Q_4K, "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"),
            VideoStream(name, VideoQuality.Q_480, "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        ))
    }

    override suspend fun getEpisodeStreams(
        title: String,
        originalTitle: String,
        season: Int,
        episode: Int
    ): Flow<List<VideoStream>> = flow {
        delay(1200)
        emit(listOf(
            VideoStream(name, VideoQuality.Q_720, "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        ))
    }
}
