package com.example

import android.Manifest
import android.os.Build
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.core.app.ActivityCompat
import androidx.core.os.LocaleListCompat
import com.example.data.repository.UserPreferencesRepository
import com.example.navigation.AppNavigation
import com.example.ui.theme.MyApplicationTheme
import com.example.utils.NotificationHelper

class MainActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    NotificationHelper.createChannel(this)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.POST_NOTIFICATIONS), 101)
    }
    enableEdgeToEdge()
    
    val userPreferences = UserPreferencesRepository(this)
    
    setContent {
      val themeMode by userPreferences.themeMode.collectAsState(initial = 0)
      val primaryColor by userPreferences.primaryColor.collectAsState(initial = 0)
      val appLanguage by userPreferences.appLanguage.collectAsState(initial = "system")
      
      // Update app language
      val currentLocales = AppCompatDelegate.getApplicationLocales()
      val desiredLanguage = if (appLanguage == "system") "" else appLanguage
      if (desiredLanguage.isNotEmpty() && currentLocales.toLanguageTags() != desiredLanguage) {
          AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(desiredLanguage))
      } else if (desiredLanguage.isEmpty() && !currentLocales.isEmpty) {
          AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
      }

      MyApplicationTheme(
          themeMode = themeMode,
          primaryColor = primaryColor
      ) {
        Surface(modifier = Modifier.fillMaxSize()) {
          AppNavigation()
        }
      }
    }
  }
}
