# app.py

import os
import subprocess
import time
import webbrowser
import requests
from models import train_model
from api import app
os.system("python -m spacy download en_core_web_sm")
FASTAPI_URL = "http://127.0.0.1:8000/docs"
@app.get("/", response_class="HTMLResponse")
async def home():
    return """
    <html>
      <head>
        <title>Email Classifier API</title>
      </head>
      <body>
        <h2>✅ Email Classifier API is Running!</h2>
        <p>Go to <a href="/docs" target="_blank">/docs</a> to test the API.</p>
      </body>
    </html>
    """


def wait_for_server(url="http://127.0.0.1:8000", timeout=15):
    print("⏳ Waiting for FastAPI server to be ready...")
    for i in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code in [404, 405]:  # Means server is up but endpoint is missing
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    print("🚀 Starting Email Classifier Project")

    if not os.path.exists("email_model.pkl"):
        print("🔧 Model not found. Training...")
        train_model()
    else:
        print("✅ Model already exists.")

    print("🌐 Launching FastAPI server...")
    subprocess.Popen(["uvicorn", "api:app", "--reload"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for the server to be ready
    if wait_for_server():
        print("🌐 Opening Swagger UI at /docs...")
        webbrowser.open(FASTAPI_URL)
    else:
        print("❌ Server didn't start in time. Try opening /docs manually.")

if __name__ == "__main__":
    main()
