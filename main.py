import asyncio
import logging

from environs import Env

logger = logging.getLogger(__name__)


async def save_message(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        chunk = await reader.readline()
        message = chunk.decode()
        print(message)


def main():
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    env = Env()
    env.read_env()
    host = env('CONNECTING_HOST')
    port = env('CONNECTING_PORT')
    asyncio.run(save_message(host, port))


if __name__ == '__main__':
    main()
