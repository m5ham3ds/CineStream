package com.example.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "download_items")
data class DownloadItem(
    @PrimaryKey val id: String,
    val title: String,
    val posterUrl: String,
    val isMovie: Boolean,
    val quality: String
)
