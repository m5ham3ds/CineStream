import re

with open("app/src/main/java/com/example/domain/models/Media.kt", "r") as f:
    content = f.read()

# Update CastMember
old_cast = """data class CastMember(
    val name: String,
    val character: String,
    val profileUrl: String?
)"""
new_cast = """data class CastMember(
    val id: String,
    val name: String,
    val character: String,
    val profileUrl: String?
)"""
content = content.replace(old_cast, new_cast)

# Add PersonDetails
person_details = """

data class PersonDetails(
    val id: String,
    val name: String,
    val biography: String,
    val profileUrl: String?,
    val birthday: String?,
    val placeOfBirth: String?,
    val knownFor: String?,
    val movies: List<Movie>,
    val series: List<Series>
)
"""
if "data class PersonDetails" not in content:
    content += person_details

with open("app/src/main/java/com/example/domain/models/Media.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "r") as f:
    repo_content = f.read()
if "getPersonDetails" not in repo_content:
    repo_content = repo_content.replace("}", """    suspend fun getPersonDetails(personId: String): com.example.domain.models.PersonDetails?\n}""")
    with open("app/src/main/java/com/example/domain/repository/MediaRepository.kt", "w") as f:
        f.write(repo_content)
