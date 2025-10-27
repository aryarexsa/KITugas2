#!/usr/bin/env python3
# Minimal WebSocket relay server (does NOT see plaintext).
# Run on Windows laptop: python ws_chat_server.py
# Requires: pip install websockets
import asyncio
import websockets
from websockets.server import WebSocketServerProtocol

CLIENTS = set()

async def handler(ws: WebSocketServerProtocol):
    CLIENTS.add(ws)
    try:
        async for msg in ws:
            # Relay ciphertext payload to all other clients
            dead = []
            for peer in CLIENTS:
                if peer is ws:
                    continue
                try:
                    await peer.send(msg)
                except:
                    dead.append(peer)
            for d in dead:
                CLIENTS.discard(d)
    finally:
        CLIENTS.discard(ws)

async def main():
    # Listen on all interfaces so the iPhone can connect over LAN
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket relay listening on ws://0.0.0.0:8765")
        print("Tip: serve client.html via any HTTP server, e.g.:")
        print("  python -m http.server 8000  (in the folder containing client.html)")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
