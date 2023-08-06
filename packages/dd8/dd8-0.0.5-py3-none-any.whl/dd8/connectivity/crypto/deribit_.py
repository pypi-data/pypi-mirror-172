# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 08:37:00 2022

@author: yqlim
"""
from typing import Union
from uuid import uuid4
from ..base import AsyncWebsocket

class DeribitWebsocket(AsyncWebsocket):
    _END_POINT = 'wss://www.deribit.com/ws/api/v2'
    _REQUEST_PER_SECOND = 20

    def __init__(self, api_key=Union[None, str], api_secret=Union[None, str], client_id=Union[None, str]):
        super().__init__(self._END_POINT)

        self.api_key = api_key
        self.api_secret = api_secret
        self.client_id = uuid4() if client_id is None else client_id
        self.msg = {'jsonrpc' : '2.0',
                    'id' : self.client_id,
                    'method' : None}

    def get_instrument(self, instrument_name: str):
        self.msg['method'] = 'public/get_instrument'
        params = {'instrument_name': instrument_name}
        self.msg['params'] = params

        return self.loop(self._get, self.msg)

    def get_instruments(self, currency, kind, expired):
        self.msg['method'] = 'public/get_instruments'
        params = {'currency': currency,
                  'kind': kind,
                  'expired': expired}
        self.msg['params'] = params

        return self.loop(self._get, self.msg)

    def get_order_book(self, instrument_name, depth):
        self.msg['method'] = 'public/get_order_book'
        params = {'instrument_name': instrument_name,
                  'depth': depth
                  }
        self.msg['params'] = params
        return self.loop(self._get, self.msg)

    def get_order_books(self, instrument_names, depth):
        self.msg['method'] = 'public/get_order_book'
        messages = []
        for instrument_name in instrument_names:
            params = {'instrument_name': instrument_name,
                      'depth': depth}
            self.msg['params'] = params
            messages.append(copy.deepcopy(self.msg))
        return asyncio.run(self.gather(self._get, messages))

    def get_index(self, currency):
        self.msg['method'] = 'public/get_index'
        params = {'currency': currency}
        self.msg['params'] = params
        return self.loop(self._get, self.msg)