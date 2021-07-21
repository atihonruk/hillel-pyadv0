from aiohttp import web


async def hello(request):
    return web.Response(text='hello, async!')


async def start(args):
    app = web.Application()
    app.add_routes([web.get('/', hello)])
    return app


web.run_app(start([]))
