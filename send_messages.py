import asyncio
import json
import logging

import aiofiles
from environs import Env

logger = logging.getLogger(__name__)


async def write_to_socket(writer, message):
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


async def register_user(reader, writer):
    await write_to_socket(writer, '\n')
    await reader.readline()
    response = await reader.readline()
    user = json.loads(response)
    nickname = user.get("nickname")
    account_hash = user.get("account_hash")
    logger.info(f'Регистрация успешно завершена, nickname: {nickname}, account_hash: {account_hash}')
    async with aiofiles.open('.env', mode='a') as file:
        await file.write(f'CHAT_TOKEN={account_hash}\n')
    logger.info('В файл `.env` добавлен CHAT_TOKEN=account_hash')


async def send_message(host, port, token, message):
    reader, writer = await asyncio.open_connection(host, port)
    if token:
        await reader.readline()
        await write_to_socket(writer, token)
        response = await reader.readline()
        user = json.loads(response)
        if user:
            logger.info(f'Вы зашли под ником: {user.get("nickname")}')
        else:
            logger.info('Невалидный токен, сейчас будет произведена регистрация')
            await register_user(reader, writer)
    else:
        logger.info('Вы не зарегистрированы, сейчас будет произведена регистрация')
        await reader.readline()
        await register_user(reader, writer)
    await write_to_socket(writer, message)
    logger.info(f'Вы отправили сообщения в чат: {message}')


def main():
    env = Env()
    env.read_env()
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)
    chat_host = env('CHAT_HOST', 'minechat.dvmn.org')
    chat_port = env.int('CHAT_PORT', 5050)
    chat_token = env('CHAT_TOKEN', '')
    asyncio.run(send_message(chat_host, chat_port, chat_token, 'Привет'))


if __name__ == '__main__':
    main()
