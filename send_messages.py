import asyncio
import logging
from environs import Env
from datetime import datetime

logger = logging.getLogger(__name__)


async def write_to_socket(writer, message):
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


async def send_message(host, port, token, message):
    reader, writer = await asyncio.open_connection(host, port)
    if token:
        response = await reader.readline()
        outgoing_message = f'[{datetime.now().strftime("%Y-%m-%d, %H:%M")}] {response.decode().rstrip()}'
        logger.info(outgoing_message)
        await write_to_socket(writer, token)
        logger.info(f'Sent message: {token}')
        response = await reader.readline()
        incoming_message = f'[{datetime.now().strftime("%Y-%m-%d, %H:%M")}] {response.decode().rstrip()}'
        logger.info(incoming_message)
    response = await reader.readline()
    incoming_message = f'[{datetime.now().strftime("%Y-%m-%d, %H:%M")}] {response.decode().rstrip()}'
    logger.info(incoming_message)
    await write_to_socket(writer, message)
    logger.info(f'Sent message: {message}')


def main():
    env = Env()
    env.read_env()
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)
    chat_host = env('CHAT_HOST', 'minechat.dvmn.org')
    chat_port = env.int('CHAT_PORT', 5050)
    chat_token = env('CHAT_TOKEN')
    asyncio.run(send_message(chat_host, chat_port, chat_token, 'Привет'))


if __name__ == '__main__':
    main()
