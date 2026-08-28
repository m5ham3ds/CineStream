package com.example.data.repository

import android.content.Context
import androidx.room.Room
import com.example.data.db.AppDatabase
import com.example.data.model.DownloadItem
import kotlinx.coroutines.flow.Flow

class DownloadRepository(context: Context) {
    private val db = Room.databaseBuilder(
        context.applicationContext,
        AppDatabase::class.java, "cinestream-db"
    ).fallbackToDestructiveMigration().build()

    private val downloadDao = db.downloadDao()

    fun getDownloadItems(): Flow<List<DownloadItem>> {
        return downloadDao.getAllItems()
    }

    suspend fun addToDownloads(item: DownloadItem) {
        downloadDao.insertItem(item)
    }

    suspend fun removeFromDownloads(item: DownloadItem) {
        downloadDao.deleteItem(item)
    }
}
