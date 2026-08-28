with open("app/src/main/java/com/example/data/remote/RetrofitClient.kt", "r") as f:
    content = f.read()

new_imports = """
import okhttp3.Cache
import okhttp3.Interceptor
import com.example.MyApplication
import java.io.File
"""

if "import okhttp3.Cache" not in content:
    content = content.replace("import okhttp3.OkHttpClient", new_imports + "import okhttp3.OkHttpClient")

new_client = """
    private val cacheSize = (10 * 1024 * 1024).toLong() // 10 MB
    private val okHttpClient by lazy {
        OkHttpClient.Builder()
            .cache(Cache(File(MyApplication.instance.cacheDir, "http_cache"), cacheSize))
            .addInterceptor { chain ->
                var request = chain.request()
                // Force cache if network is unavailable. For simplicity, we just add max-stale.
                // In a real app we'd check ConnectivityManager, but forcing a tolerant cache-control works for TMDB which is mostly static.
                request = request.newBuilder()
                    .header("Cache-Control", "public, max-age=" + 60 + ", max-stale=" + 60 * 60 * 24 * 7)
                    .build()
                chain.proceed(request)
            }
            .addInterceptor(loggingInterceptor)
            .build()
    }
"""

if "cacheSize" not in content:
    content = content.replace("    private val okHttpClient = OkHttpClient.Builder()\n        .addInterceptor(loggingInterceptor)\n        .build()", new_client)

with open("app/src/main/java/com/example/data/remote/RetrofitClient.kt", "w") as f:
    f.write(content)
