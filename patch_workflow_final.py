import re

filepath = '.github/workflows/build.yml'
with open(filepath, 'r') as f:
    content = f.read()

# Replace google-services.json setup step
replacement = """      - name: Setup google-services.json
        run: |
          echo "ewogICJwcm9qZWN0X2luZm8iOiB7CiAgICAicHJvamVjdF9udW1iZXIiOiAiOTc5NDQ3MjU2NDE4IiwKICAgICJwcm9qZWN0X2lkIjogImNpbmVzdHJlYW0tc3VsbyIsCiAgICAic3RvcmFnZV9idWNrZXQiOiAiY2luZXN0cmVhbS1zdWxvLmZpcmViYXNlc3RvcmFnZS5hcHAiCiAgfSwKICAiY2xpZW50IjogWwogICAgewogICAgICAiY2xpZW50X2luZm8iOiB7CiAgICAgICAgIm1vYmlsZXNka19hcHBfaWQiOiAiMTo5Nzk0NDcyNTY0MTg6YW5kcm9pZDowMzdhOWIzYTEzOTNlNTUwYTk4ODNiIiwKICAgICAgICAiYW5kcm9pZF9jbGllbnRfaW5mbyI6IHsKICAgICAgICAgICJwYWNrYWdlX25hbWUiOiAiY29tLmFpc3R1ZGlvLmNpbmVzdHJlYW0ueHl6YWJjIgogICAgICAgIH0KICAgICAgfSwKICAgICAgIm9hdXRoX2NsaWVudCI6IFsKICAgICAgICB7CiAgICAgICAgICAiY2xpZW50X2lkIjogIjk3OTQ0NzI1NjQxOC05amw0Y2w5NGYyMmEyMjdzdHJ2aGozdXBzOThkcGthMC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsCiAgICAgICAgICAiY2xpZW50X3R5cGUiOiAxLAogICAgICAgICAgImFuZHJvaWRfaW5mbyI6IHsKICAgICAgICAgICAgInBhY2thZ2VfbmFtZSI6ICJjb20uYWlzdHVkaW8uY2luZXN0cmVhbS54eXphYmMiLAogICAgICAgICAgICAiY2VydGlmaWNhdGVfaGFzaCI6ICIxZTBmNGE0YTBlZTg0YjcwMjNlNTk1MDRiM2E5NzgzODJkMDE5ZTJhIgogICAgICAgICAgfQogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgImNsaWVudF9pZCI6ICI5Nzk0NDcyNTY0MTgtcmpiOWEwOTkxZ3Z2ZTAzMjhuMTEzZG1lNjdpNGdwdjIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLAogICAgICAgICAgImNsaWVudF90eXBlIjogMwogICAgICAgIH0KICAgICAgXSwKICAgICAgImFwaV9rZXkiOiBbCiAgICAgICAgewogICAgICAgICAgImN1cnJlbnRfa2V5IjogIkFJemFTeUM5Q3ZhTTlNdzNOaUQtS3NPaVl2SFpIajZYWkpRSm5QcyIKICAgICAgICB9CiAgICAgIF0sCiAgICAgICJzZXJ2aWNlcyI6IHsKICAgICAgICAiYXBwaW52aXRlX3NlcnZpY2UiOiB7CiAgICAgICAgICAib3RoZXJfcGxhdGZvcm1fb2F1dGhfY2xpZW50IjogWwogICAgICAgICAgICB7CiAgICAgICAgICAgICAgImNsaWVudF9pZCI6ICI5Nzk0NDcyNTY0MTgtcmpiOWEwOTkxZ3Z2ZTAzMjhuMTEzZG1lNjdpNGdwdjIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLAogICAgICAgICAgICAgICJjbGllbnRfdHlwZSI6IDMKICAgICAgICAgICAgfQogICAgICAgICAgXQogICAgICAgIH0KICAgICAgfQogICAgfQogIF0sCiAgImNvbmZpZ3VyYXRpb25fdmVyc2lvbiI6ICIxIgp9Cg==" | base64 -d > app/google-services.json"""

content = re.sub(
    r"      - name: Setup google-services\.json.*?          fi",
    replacement,
    content,
    flags=re.DOTALL
)

# Force the environment variable for WEB_CLIENT_ID
env_replacement = """      - name: Build Debug APK
        env:
          WEB_CLIENT_ID: "979447256418-rjb9a0991gvve0328n113dme67i4gpv2.apps.googleusercontent.com"
        run: ./gradlew assembleDebug"""

content = re.sub(
    r"      - name: Build Debug APK\n        run: \./gradlew assembleDebug",
    env_replacement,
    content
)

with open(filepath, 'w') as f:
    f.write(content)
