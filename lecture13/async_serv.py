import asyncio


# def countdown(n):
#     while n > 0:
#         yield n
#         n =- 1


async def echo_handler(reader, writer):
    while True:
        data = await reader.read(256) #  blocking
        if not data:
            break
        arg = int(data)
        res =  rfib(arg)
        await writer.write((str(res) + '\n').encode())  # blocking
    writer.close() # flush


async def main():
    server = await asyncio.start_server(echo_handler, host='127.0.0.1', port=5000)

    async with server:
        await server.serve_forever()

asyncio.run(main())
