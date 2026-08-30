import re

filepath = '.github/workflows/build.yml'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """      - name: Setup google-services.json
        env:
          GOOGLE_SERVICES_JSON: ${{ secrets.GOOGLE_SERVICES_JSON }}
        run: |
          if [ -n "$GOOGLE_SERVICES_JSON" ]; then
            echo "Found GOOGLE_SERVICES_JSON secret. Writing to file."
            echo "$GOOGLE_SERVICES_JSON" > app/google-services.json
          elif [ -f "app/google-services.json" ]; then
            echo "google-services.json already exists in repo. Using it."
          else
            echo "No GOOGLE_SERVICES_JSON secret found. Creating dummy file for compilation."
            echo '{"project_info":{"project_number":"123456789","project_id":"dummy-project"},"client":[{"client_info":{"mobilesdk_app_id":"1:123456789:android:abcdef","android_client_info":{"package_name":"com.aistudio.cinestream.xyzabc"}},"api_key":[{"current_key":"dummy_key"}]}]}' > app/google-services.json
          fi"""

content = re.sub(
    r"      - name: Setup google-services\.json\n        env:\n          GOOGLE_SERVICES_JSON: \$\{\{ secrets\.GOOGLE_SERVICES_JSON \}\}\n        run: \|\n          if \[ -z \"\$GOOGLE_SERVICES_JSON\" \]; then\n            echo \"No GOOGLE_SERVICES_JSON secret found\. Creating dummy file for compilation\.\"\n            echo '.*?' > app/google-services\.json\n          else\n            echo \"Found GOOGLE_SERVICES_JSON secret\. Writing to file\.\"\n            echo \"\$GOOGLE_SERVICES_JSON\" > app/google-services\.json\n          fi",
    replacement,
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)
