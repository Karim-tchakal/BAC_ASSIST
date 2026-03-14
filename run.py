import threading
import webview
import uvicorn
from main import app

def start():
    uvicorn.run(app, host="127.0.0.1", port=8000)

threading.Thread(target=start).start()
webview.create_window("My App", "http://127.0.0.1:8000")
webview.start()