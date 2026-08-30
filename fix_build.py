import re
with open('app/build.gradle.kts', 'r') as f:
    c = f.read()
c = c.replace("// implementation(libs.firebase.firestore)", "implementation(libs.firebase.firestore)")
c = c.replace("// implementation(libs.firebase.auth)", "implementation(libs.firebase.auth)")
c = c.replace("// implementation(libs.androidx.credentials)", "implementation(libs.androidx.credentials)")
c = c.replace("// implementation(libs.androidx.credentials.play.services)", "implementation(libs.androidx.credentials.play.services)")
c = c.replace("// implementation(libs.googleid)", "implementation(libs.googleid)")
with open('app/build.gradle.kts', 'w') as f:
    f.write(c)
