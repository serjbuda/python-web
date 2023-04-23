import argparse
import asyncio
import datetime
import json
import websockets

from typing import List, Dict
from aiohttp import ClientSession
from aiofile import AIOFile, Writer

class ExchangeRateService:
    @staticmethod
    async def fetch_exchange_rates(currencies: List[str], days: int) -> List[Dict]:
        async with ClientSession() as session:
            today = datetime.date.today()
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={today.strftime("%d.%m.%Y")}'
            response = await session.get(url)
            json_response = await response.json()

            exchange_rates = []
            for day in range(1, days+1):
                target_date = today - datetime.timedelta(days=day)
                url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={target_date.strftime("%d.%m.%Y")}'
                response = await session.get(url)
                json_data = await response.json()
                if 'exchangeRate' not in json_data:
                    continue

                rates = {'date': target_date.strftime('%d.%m.%Y')}
                for rate in json_data['exchangeRate']:
                    if rate['currency'] in currencies:
                        rates[rate['currency']] = {
                            'purchase': rate['purchaseRateNB'],
                            'sale': rate['saleRateNB']
                        }
                exchange_rates.append(rates)
        return exchange_rates

class ChatServer:
    def __init__(self):
        self.clients = set()

    async def register(self, ws):
        self.clients.add(ws)
        print(f'{ws.remote_address} joined chat')

    async def broadcast(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def exchange_rate(self, message):
        try:
            parts = message.strip().split()
            if len(parts) < 2 or parts[0] != 'exchange':
                await self.broadcast('Invalid command. Usage: exchange [days] [currency1] [currency2] ...')
                return

            days = int(parts[1])
            if days > 10:
                await self.broadcast('Maximum number of days is 10')
                return

            currencies = parts[2:]
            if not currencies:
                currencies = ['USD', 'EUR']

            rates = await ExchangeRateService.fetch_exchange_rates(currencies, days)

            if not rates:
                await self.broadcast('Exchange rates not available')
                return

            response = json.dumps(rates)
            await self.broadcast(response)

            # Logging
            await self.log_exchange(message)
        except ValueError:
            await self.broadcast('Days argument must be an integer')
        except Exception as e:
            await self.broadcast(f'Error: {e}')

    async def log_exchange(self, message):
        async with AIOFile('exchange.log', 'a') as afp:
            async with Writer(afp) as writer:
                writer.write(f'{datetime.datetime.now()} {message}\n')


async def handle_client(websocket, path):
    await chat_server.register(websocket)
    try:
        async for message in websocket:
            await chat_server.exchange_rate(message)
    finally:
        chat_server.clients.remove(websocket)
        print(f'{websocket.remote_address} left chat')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get exchange rates from PrivatBank API.')
    parser.add_argument('days', type=int, default=10, nargs='?', help='number of days to get exchange rates for')
    parser.add_argument('--currencies', '-c', nargs='*', default=['USD', 'EUR'], help='currencies to get exchange rates for')
