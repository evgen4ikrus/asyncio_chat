import asyncio
import logging
from datetime import datetime

import aiofiles
from environs import Env

logger = logging.getLogger(__name__)


async def save_message(host, port, file_name):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        chunk = await reader.readline()
        message = f'[{datetime.now().strftime("%Y-%m-%d, %H:%M")}] {chunk.decode()}'
        print(message)
        async with aiofiles.open(file_name, mode='a') as file:
            await file.write(message)


def main():
    message_history_file = 'message_history.txt'
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    env = Env()
    env.read_env()
    host = env('CONNECTING_HOST')
    port = env('CONNECTING_PORT')
    asyncio.run(save_message(host, port, message_history_file))


if __name__ == '__main__':
    main()
