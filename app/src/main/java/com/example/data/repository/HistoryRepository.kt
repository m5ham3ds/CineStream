package com.example.data.repository
import android.content.Context
import androidx.room.Room
import com.example.data.db.AppDatabase
import com.example.data.model.HistoryItem
import kotlinx.coroutines.flow.Flow

class HistoryRepository(context: Context) {
    private val db = Room.databaseBuilder(
        context.applicationContext,
        AppDatabase::class.java, "cinestream-db"
    ).fallbackToDestructiveMigration().build()
    private val historyDao = db.historyDao()

    fun getHistoryItems(): Flow<List<HistoryItem>> = historyDao.getAllHistory()

    suspend fun addToHistory(item: HistoryItem) {
        historyDao.insertHistory(item)
    }
}
