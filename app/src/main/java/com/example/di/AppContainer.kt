package com.example.di

import com.example.data.repository.MockMediaRepositoryImpl
import com.example.domain.repository.MediaRepository

object AppContainer {
    val mediaRepository: MediaRepository by lazy {
        MockMediaRepositoryImpl()
    }
}
