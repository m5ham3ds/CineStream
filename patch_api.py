with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    content = f.read()

new_endpoint = """
    @GET("person/{person_id}")
    suspend fun getPersonDetails(
        @Path("person_id") personId: Int,
        @Query("api_key") apiKey: String,
        @Query("append_to_response") appendToResponse: String = "combined_credits"
    ): TmdbPersonDetails
}"""
content = content.replace("}", new_endpoint)

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(content)
