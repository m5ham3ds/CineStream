package com.example.data.db

import androidx.room.Database
import androidx.room.RoomDatabase
import com.example.data.model.LibraryItem
import com.example.data.model.DownloadItem

@Database(entities = [LibraryItem::class, DownloadItem::class, com.example.data.model.HistoryItem::class], version = 2, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun libraryDao(): LibraryDao
    abstract fun downloadDao(): DownloadDao
    abstract fun historyDao(): HistoryDao
}
