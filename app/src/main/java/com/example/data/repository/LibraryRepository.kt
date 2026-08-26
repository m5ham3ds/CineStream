package com.example.data.repository

import android.content.Context
import androidx.room.Room
import com.example.data.db.AppDatabase
import com.example.data.model.LibraryItem
import kotlinx.coroutines.flow.Flow

class LibraryRepository(context: Context) {
    private val db = Room.databaseBuilder(
        context.applicationContext,
        AppDatabase::class.java, "cinestream-db"
    ).build()

    private val libraryDao = db.libraryDao()

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
