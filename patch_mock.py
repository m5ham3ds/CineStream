with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "r") as f:
    content = f.read()

if "getPersonDetails" not in content:
    content = content.replace("}", "    override suspend fun getPersonDetails(personId: String): com.example.domain.models.PersonDetails? = null\n}")
    with open("app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt", "w") as f:
        f.write(content)
