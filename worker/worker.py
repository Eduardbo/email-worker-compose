import json
import os
from random import randint
from time import sleep

import redis


if __name__ == '__main__':
    redis_host = os.getenv('REDIS_HOST', 'queue')
    r = redis.Redis(host=redis_host, port=6379, db=0)

    print('Aguardando mensagens ...')

    while True:
        item = r.blpop('sender')
        if item is None:
            continue

        mensagem = json.loads(item[1])
        print('Mandando a mensagem:', mensagem['assunto'])
        sleep(randint(15, 45))
        print('Mensagem', mensagem['assunto'], 'enviada')