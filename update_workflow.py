import re

with open('.github/workflows/build.yml', 'r') as f:
    content = f.read()

new_step = """      - name: Setup google-services.json
        env:
          GOOGLE_SERVICES_JSON: ${{ secrets.GOOGLE_SERVICES_JSON }}
        run: |
          if [ -z "$GOOGLE_SERVICES_JSON" ]; then
            echo "No GOOGLE_SERVICES_JSON secret found. Creating dummy file for compilation."
            echo '{"project_info":{"project_number":"123456789","project_id":"dummy-project"},"client":[{"client_info":{"mobilesdk_app_id":"1:123456789:android:abcdef","android_client_info":{"package_name":"com.aistudio.cinestream.xyzabc"}},"api_key":[{"current_key":"dummy_key"}]}]}' > app/google-services.json
          else
            echo "Found GOOGLE_SERVICES_JSON secret. Writing to file."
            echo "$GOOGLE_SERVICES_JSON" > app/google-services.json
          fi"""

# replace the dummy step
content = re.sub(r'      - name: Create dummy google-services\.json.*?app/google-services\.json', new_step, content, flags=re.DOTALL)

with open('.github/workflows/build.yml', 'w') as f:
    f.write(content)
