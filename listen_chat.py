import argparse
import asyncio
import logging
import time
from datetime import datetime

import aiofiles
from environs import Env

from tcp_tools import open_connection

logger = logging.getLogger(__name__)

failed_connection_attempts = 0


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
    global failed_connection_attempts
    async with open_connection(host, port) as connection:
        reader, writer = connection
        failed_connection_attempts = 0
        while True:
            chunk = await reader.readline()
            message = f'[{datetime.now().strftime("%Y-%m-%d, %H:%M")}] {chunk.decode().rstrip()}'
            if enabled_console:
                logger.info(message)
            async with aiofiles.open(file_path, mode='a') as file:
                await file.write(f'{message}\n')


def main():
    env = Env()
    env.read_env()
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)
    possible_host, possible_port, possible_message_history_path, enabled_console = get_args()
    chat_host = possible_host or env('CHAT_HOST', 'minechat.dvmn.org')
    listening_messages_chat_port = possible_port or env.int('LISTENING_MESSAGES_CHAT_PORT', 5000)
    message_history_path = possible_message_history_path or env('MESSAGE_HISTORY_PATH', 'message_history.txt')
    global failed_connection_attempts
    while True:
        try:
            asyncio.run(save_message(chat_host, listening_messages_chat_port, message_history_path, enabled_console))
        except KeyboardInterrupt:
            logger.info('Вы остановили соединение')
            break
        except:
            if failed_connection_attempts:
                time.sleep(10)
            failed_connection_attempts += 1
            logger.error('Произошла ошибка, пробуем переподключиться к чату...')


if __name__ == '__main__':
    main()
