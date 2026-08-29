package com.example.data.repository

import android.content.Context
import androidx.room.Room
import com.example.data.db.AppDatabase
import com.example.data.model.LibraryItem
import kotlinx.coroutines.flow.Flow

class LibraryRepository(context: Context) {
    private val db = AppDatabase.getDatabase(context)

    private val libraryDao = db.libraryDao()

    fun isItemInLibrary(id: String): Flow<Boolean> = libraryDao.isItemInLibrary(id)

    fun getLibraryItems(): Flow<List<LibraryItem>> {
        return libraryDao.getAllItems()
    }

    suspend fun addToLibrary(item: LibraryItem) {
        libraryDao.insertItem(item)
    }

    suspend fun removeFromLibrary(item: LibraryItem) {
        libraryDao.deleteItem(item)
    }
}
