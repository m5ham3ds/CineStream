import re

# Update libs.versions.toml
with open('gradle/libs.versions.toml', 'r') as f:
    toml = f.read()

if 'playServicesNearby' not in toml:
    toml = toml.replace(
        '[versions]\n',
        '[versions]\nplayServicesNearby = "19.0.0"\n'
    )
    toml = toml.replace(
        '[libraries]\n',
        '[libraries]\nplay-services-nearby = { module = "com.google.android.gms:play-services-nearby", version.ref = "playServicesNearby" }\n'
    )
    with open('gradle/libs.versions.toml', 'w') as f:
        f.write(toml)

# Update build.gradle.kts
with open('app/build.gradle.kts', 'r') as f:
    gradle = f.read()

if 'play-services-nearby' not in gradle:
    gradle = gradle.replace(
        'dependencies {',
        'dependencies {\n    implementation(libs.play.services.nearby)'
    )
    with open('app/build.gradle.kts', 'w') as f:
        f.write(gradle)

# Update AndroidManifest.xml
manifest_path = 'app/src/main/AndroidManifest.xml'
with open(manifest_path, 'r') as f:
    manifest = f.read()

perms = """
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADVERTISE" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
    <uses-permission android:name="android.permission.NEARBY_WIFI_DEVICES" />
"""

if 'android.permission.BLUETOOTH_CONNECT' not in manifest:
    manifest = manifest.replace(
        '<application',
        perms + '\n    <application'
    )
    with open(manifest_path, 'w') as f:
        f.write(manifest)

