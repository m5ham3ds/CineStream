package com.example.data.repository

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.WatchedEpisode
import kotlinx.coroutines.flow.Flow

class WatchedEpisodeRepository(context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val dao = db.watchedEpisodeDao()

    fun getAllWatched(): Flow<List<WatchedEpisode>> = dao.getAllWatched()

    suspend fun markAsWatched(id: String) {
        dao.insert(WatchedEpisode(id))
    }

    suspend fun markAsUnwatched(id: String) {
        dao.deleteById(id)
    }
}
