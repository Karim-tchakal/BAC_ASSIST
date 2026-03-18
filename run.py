import threading
import uvicorn
import webbrowser
from main import app

def start():
    uvicorn.run(app, host="127.0.0.1", port=8000)

threading.Thread(target=start, daemon=True).start()

webbrowser.open("http://127.0.0.1:8000")

# Keep the script running
threading.Event().wait()