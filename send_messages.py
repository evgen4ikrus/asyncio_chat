import asyncio

from environs import Env


async def send_message(host, port, token):
    reader, writer = await asyncio.open_connection(host, port)
    message = f'{token}\n'
    writer.write(message.encode())
    await writer.drain()
    while True:
        message = f'{input()}\n\n'
        writer.write(message.encode())
        await writer.drain()


def main():
    env = Env()
    env.read_env()
    chat_host = env('CHAT_HOST', 'minechat.dvmn.org')
    chat_port = env.int('CHAT_PORT', 5050)
    chat_token = env('CHAT_TOKEN')
    asyncio.run(send_message(chat_host, chat_port, chat_token))


if __name__ == '__main__':
    main()
