package com.example.data.repository

import android.content.Context
import androidx.room.Room
import com.example.data.db.AppDatabase
import com.example.data.model.DownloadItem
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

class DownloadRepository(context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val downloadDao = db.downloadDao()
    private val scope = CoroutineScope(Dispatchers.IO)

    fun getDownloadItems(): Flow<List<DownloadItem>> {
        return downloadDao.getAllItems()
    }

    suspend fun addToDownloads(item: DownloadItem) {
        downloadDao.insertItem(item)
        startSimulatedDownload(item.id)
    }

    suspend fun updateDownload(item: DownloadItem) {
        downloadDao.updateItem(item)
    }

    suspend fun removeFromDownloads(item: DownloadItem) {
        downloadDao.deleteItem(item)
    }

    private fun startSimulatedDownload(id: String) {
        scope.launch {
            var currentItem = downloadDao.getItemById(id) ?: return@launch
            
            while (currentItem.progress < 1f && !currentItem.isCompleted) {
                delay(1000) // update every second
                
                // Re-fetch to check if paused or deleted
                currentItem = downloadDao.getItemById(id) ?: return@launch
                
                if (currentItem.isPaused) continue
                
                val newProgress = (currentItem.progress + 0.05f).coerceAtMost(1f)
                val isCompleted = newProgress >= 1f
                
                currentItem = currentItem.copy(
                    progress = newProgress,
                    isCompleted = isCompleted
                )
                
                downloadDao.updateItem(currentItem)
            }
        }
    }
}
