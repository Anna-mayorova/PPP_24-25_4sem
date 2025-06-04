from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_email: str):
        await websocket.accept()
        if user_email not in self.active_connections:
            self.active_connections[user_email] = []
        self.active_connections[user_email].append(websocket)

    def disconnect(self, websocket: WebSocket, user_email: str):
        self.active_connections[user_email].remove(websocket)
        if not self.active_connections[user_email]:
            del self.active_connections[user_email]

    async def send_message(self, message: dict, user_email: str):
        for connection in self.active_connections.get(user_email, []):
            await connection.send_json(message)

manager = ConnectionManager()