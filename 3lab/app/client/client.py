import asyncio
import websockets
import json

async def run_client():
    token = input("Enter your JWT token: ")
    uri = f"ws://localhost:8000/ws/connect?token={token}"


    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with websockets.connect(uri) as websocket: # async with websockets.connect(uri) as websocket:


        #
            print("Connected to WebSocket server.")

            async def listen():
                while True:
                    try:
                        response = await websocket.recv()
                        print(f"[NOTIFICATION] {response}")
                    except websockets.ConnectionClosed:
                        print("[INFO] Connection closed by server.")
                        break

            listener_task = asyncio.create_task(listen())

            print("You can now send commands. Type 'exit' to quit.")
            while True:
                cmd = input("Enter command: ").strip()

                if cmd == "exit":
                    print("Exiting...")
                    break
                elif cmd.startswith("solve"):
                    try:
                        _, nodes_str, edges_str = cmd.split(" ", 2)
                        nodes = json.loads(nodes_str)
                        edges = json.loads(edges_str)
                        payload = {
                            "task_id": "manual_" + str(hash(cmd)),
                            "nodes": nodes,
                            "edges": edges
                        }
                        await websocket.send(json.dumps(payload))
                        print("Sent task to server.")
                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Failed to parse JSON: {e}")
                    except Exception as e:
                        print(f"[ERROR] {e}")
                else:
                    print("Unknown command. Use 'solve [nodes] [edges]' or 'exit'")

            listener_task.cancel()
            try:
                await listener_task
            except asyncio.CancelledError:
                pass

    except websockets.exceptions.WebSocketException as e:
        print(f"[ERROR] WebSocket connection failed: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(run_client())