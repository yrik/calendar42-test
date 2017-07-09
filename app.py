import os

import asyncio

from aiohttp import web, client_exceptions, ClientSession

from aiocache import SimpleMemoryCache


BASE_URL = "https://demo.calendar42.com/api/v2"
TOKEN = os.environ.get('CALENDAR42_TOKEN')


# NOTE: use redis in production
cache = SimpleMemoryCache(timeout=260)  # 4.2 min


async def fetch(url, session):
    """
    Returns JSON content of the page.
    """
    cached = await cache.get(url)
    if cached:
        return cached

    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Token {token}'.format(token=TOKEN),
    }
    async with session.get(url, headers=headers) as response:
        data = await response.json()
        if response.status == 200:
             await cache.set(url, data)
        else:
            await cache.delete(url)
        return data


async def event_with_subscriptions(request):
    """
    Returns combined event and subscriptions data for given event_id.
    """
    event_id = request.match_info.get('event_id')

    tasks = []
    async with ClientSession() as session:

        url = BASE_URL + '/events/{event_id}/'.format(event_id=event_id)
        task = asyncio.ensure_future(fetch(url, session))
        tasks.append(task)

        url = BASE_URL + '/event-subscriptions/?event_ids=[{event_id}]'.format(event_id=event_id)
        task = asyncio.ensure_future(fetch(url, session))
        tasks.append(task)

        try:
            event, subscribers = await asyncio.gather(*tasks)
        except client_exceptions.ClientResponseError:
            data = {'error': {'status_code': 500, 'message': 'Can not get response from Calendar42'}}
            return web.json_response(data, status=500)

        if 'error' in event:
            return web.json_response(event, status=event['error']['status_code'])
        if 'error' in subscribers:
            return web.json_response(subscribers, status=subscribers['error']['status_code'])

        data = {
            'id': event_id,
            'title': event['data'][0]['title'],
            'names': [item['subscriber']['first_name'] for item in subscribers['data']],
        }
        return web.json_response(data)


app = web.Application()
app.router.add_get('/event-with-subscriptions/{event_id}', event_with_subscriptions)


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
