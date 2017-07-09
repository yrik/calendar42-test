from aiohttp import web


async def handle(request):
    event_id = request.match_info.get('event_id')
    return web.Response(text=event_id)


app = web.Application()
app.router.add_get('/events-with-subscriptions/{event_id}', handle)

web.run_app(app, host='127.0.0.1', port=8080)
