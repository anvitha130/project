import os
import google.generativeai as genai

# Get API key from environment
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment")
    print("Set it in PowerShell with:")
    print('$env:GOOGLE_API_KEY = "your-api-key-here"')
    raise SystemExit(1)

print(f"✓ Found API key (starts with: {api_key[:8]}...)")

# Try to configure and make a test call
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content("Say hi!")
    print("✓ API test successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ API test failed: {str(e)}")
    raise