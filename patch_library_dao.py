import re

with open("app/src/main/java/com/example/data/db/LibraryDao.kt", "r") as f:
    content = f.read()

content = content.replace("fun getAllItems(): Flow<List<LibraryItem>>", "fun getAllItems(): Flow<List<LibraryItem>>\n\n    @Query(\"SELECT EXISTS(SELECT * FROM library_items WHERE id = :id)\")\n    fun isItemInLibrary(id: String): Flow<Boolean>")

with open("app/src/main/java/com/example/data/db/LibraryDao.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/data/repository/LibraryRepository.kt", "r") as f:
    content = f.read()

content = content.replace("fun getLibraryItems(): Flow<List<LibraryItem>> {", "fun isItemInLibrary(id: String): Flow<Boolean> = libraryDao.isItemInLibrary(id)\n\n    fun getLibraryItems(): Flow<List<LibraryItem>> {")

with open("app/src/main/java/com/example/data/repository/LibraryRepository.kt", "w") as f:
    f.write(content)
