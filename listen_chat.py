import argparse
import asyncio
import logging
from datetime import datetime

import aiofiles
from environs import Env

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='хост чата;')
    parser.add_argument('--port', help='порт чата:')
    parser.add_argument('--history', help='путь до файла для сохранения истории сообщений;')
    parser.add_argument('--disable_console', default=True, action='store_false',
                        help='отключить вывод сообщений в консоль.')
    args = parser.parse_args()
    return args.host, args.port, args.history, args.disable_console


async def save_message(host, port, file_path, enabled_console):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        chunk = await reader.readline()
        message = f'[{datetime.now().strftime("%Y-%m-%d, %H:%M")}] {chunk.decode()}'
        if enabled_console:
            logger.info(message)
        async with aiofiles.open(file_path, mode='a') as file:
            await file.write(message)


def main():
    env = Env()
    env.read_env()
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    possible_host, possible_port, possible_message_history_path, enabled_console = get_args()
    host = possible_host or env('CONNECTING_HOST', 'minechat.dvmn.org')
    port = possible_port or env.int('CONNECTING_PORT', 5000)
    message_history_path = possible_message_history_path or env('MESSAGE_HISTORY_PATH', 'message_history.txt')
    asyncio.run(save_message(host, port, message_history_path, enabled_console))


if __name__ == '__main__':
    main()
