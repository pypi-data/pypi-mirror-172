# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 12:23:41 2022

@author: yqlim
"""

from typing import List, Dict, Callable
import json
import asyncio
from aiohttp import ClientSession
import websockets

class AsyncConnection(object):
    def __init__(self) -> None:
        pass

    async def _get(self, url: str, params: Dict = {}) -> Dict:
        async with ClientSession() as sess:
            async with sess.get(url, params=params) as resp:
                response = await resp.json()
        return response

    async def _post(self, url: str):
        pass

    async def _put(self, url: str):
        pass

    async def gather(self, requestor: Callable, messages: List[str]) -> List[Dict]:
        response = await asyncio.gather(*[requestor(msg) for msg in messages])
        return response

    def loop(self, get, url) -> Dict:
        response = asyncio.run(get(url))
        return response

class AsyncWebsocket(AsyncConnection):
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    async def _get(self, url: str):
        async with websockets.connect(self.endpoint) as websocket:
            await websocket.send(url)
            while websocket.open:
                response = await websocket.recv()
                response = json.loads(response)
                return response