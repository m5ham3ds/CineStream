with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "val allMoviesDeferred = async" in line:
        new_lines.append("                val allSeriesDeferred = async { repository.getSeries().firstOrNull() ?: emptyList() }\n")
    elif "val allMovies = allMoviesDeferred.await()" in line:
        new_lines.append("                val allSeries = allSeriesDeferred.await()\n")
    elif "actionMovies = actionMovies," in line:
        new_lines.append("                        allMovies = allMovies,\n")
        new_lines.append("                        allSeries = allSeries,\n")

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.writelines(new_lines)
