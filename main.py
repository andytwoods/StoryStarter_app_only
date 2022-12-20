from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/browser_ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


browser_websocket: WebSocket
android_websocket: WebSocket


@app.websocket("/browser_ws")
async def browser_websocket_endpoint(_browser_websocket: WebSocket):
    global browser_websocket, android_websocket
    browser_websocket = _browser_websocket
    await browser_websocket.accept()
    while True:
        data = await browser_websocket.receive_text()
        # Abdi, we can run code here
        try:
            await android_websocket.send_text(data)
            await browser_websocket.send_text(f"SENT TO ANDROID: {data}")
        except NameError:
            await browser_websocket.send_text(f"NOT SENT TO ANDROID: {data}")


@app.websocket("/android_ws")
async def android_websocket_endpoint(_android_websocket: WebSocket):
    global android_websocket, browser_websocket
    android_websocket = _android_websocket
    await android_websocket.accept()
    while True:
        data = await android_websocket.receive_text()
        # Abdi, we can run code here
        try:
            await browser_websocket.send_text(data)
            await android_websocket.send_text(f"SENT TO BROWSER: {data}")
        except NameError:
            await android_websocket.send_text(f"NOT SENT TO BROWSER: {data}")
