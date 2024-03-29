import argparse
import asyncio
import json
import logging

import aiofiles
from environs import Env

from tcp_tools import open_connection

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('message', help='отправляемое в чат сообщение')
    parser.add_argument('--host', help='хост чата')
    parser.add_argument('--port', help='порт чата для отправки сообщения')
    parser.add_argument('--token', help='токен пользователя чата')
    parser.add_argument('--username', help='username для регистрации в чате')
    args = parser.parse_args()
    return args.message, args.host, args.port, args.token, args.username


async def write_to_socket(writer, message):
    writer.write(f'{message}\n'.encode())
    await writer.drain()


async def authorise(reader, writer, token, username):
    await write_to_socket(writer, token)
    response = await reader.readline()
    user = json.loads(response)
    if user:
        logger.info(f'Вы зашли под ником: {user.get("nickname")}')
    else:
        logger.info('Невалидный токен, сейчас будет произведена регистрация')
        await register_user(reader, writer, username)


async def register_user(reader, writer, username):
    await reader.readline()
    await write_to_socket(writer, username)
    response = await reader.readline()
    user = json.loads(response)
    nickname = user.get("nickname")
    account_hash = user.get("account_hash")
    logger.info(f'Регистрация успешно завершена, nickname: {nickname}, account_hash: {account_hash}')
    async with aiofiles.open('.env', mode='a') as file:
        await file.write(f'USER_CHAT_TOKEN={account_hash}\n')
    logger.info('В файл `.env` добавлен CHAT_TOKEN=account_hash')


async def send_message(host, port, token, message, username):
    async with open_connection(host, port) as connection:
        reader, writer = connection
        await reader.readline()
        if token:
            await authorise(reader, writer, token, username)
        else:
            logger.info('Вы не зарегистрированы, сейчас будет произведена регистрация')
            await write_to_socket(writer, '\n')
            await register_user(reader, writer, username)
        await write_to_socket(writer, f'{message}\n')
        logger.info(f'Вы отправили сообщения в чат: {message}')


def main():
    env = Env()
    env.read_env()
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level=logging.DEBUG)
    message, possible_host, possible_port, possible_token, possible_username = get_args()
    chat_host = possible_host or env('CHAT_HOST', 'minechat.dvmn.org')
    sending_message_chat_port = possible_port or env.int('SENDING_MESSAGE_CHAT_PORT', 5050)
    user_chat_token = possible_token or env('USER_CHAT_TOKEN', '')
    chat_username = possible_username or env('CHAT_USERNAME', '')
    asyncio.run(send_message(chat_host, sending_message_chat_port, user_chat_token, message, chat_username))


if __name__ == '__main__':
    main()
