# Asyncio_chat
## Микросервис listen_chat
Создает TCP-подключение с чатом, выводит сообщения чата в консоль и сохраняет историю сообщений в файл.
#### Запуск

```commandline
python3 listen_chat.py
```

#### Переменные окружения:
Создайте файл `.env` и задайте значения переменных в формате КЛЮЧ=ЗНАЧЕНИЕ:
``` dotenv
`CONNECTING_HOST` - хост чата; # default: minechat.dvmn.org
`CONNECTING_PORT` - порт чата; # default: 5000
`MESSAGE_HISTORY_PATH` - путь до файла для сохранения истории сообщений. # default: message_history.txt
```
#### Дополнительные аргументы командной строки:
Микросервис принимает дополнительные аргументы через командную строку.
Для получения информации введите:

```commandline
python3 listen_chat.py --help
```
