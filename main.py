import json
import logging
from random import choice
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


def handle_dialog(res, req):
    if req['session']['new']:
        res['response']['text'] = 'Привет. Купи слона!'
        return
    if req['state']['session']:
        if len(set(
                req['request']['nlu']['tokens']) - {'ладно', 'куплю', 'покупаю', 'хорошо'}) != len(
            set(req['request']['nlu']['tokens'])):
            res['reponse']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
            res['response']['buttons'] = [{'title': 'Посмотреть',
                                           'url': 'https://market.yandex.ru/search?cvredirect=2&suggest_reqid=91938777584344923039168083875807&text=кролик'}]
            return
        else:
            user_answ = req['resquest']['command']
            res['response']['text'] = f'Все гвороят {user_answ}, а ты купи кролика'
        res['response']['buttons'] = [{'title': choice(['ладно', 'куплю', 'покупаю', 'хорошо'])}]
        res['session_state']['rabbit'] = True
        return
    if len(set(req['request']['nlu']['tokens']) - {'ладно', 'куплю', 'покупаю', 'хорошо'}) != len(
            set(req['request']['nlu']['tokens'])):
        res['reponse']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
        res['response']['buttons'] = [{'title': 'Посмотреть',
                                       'url': 'https://market.yandex.ru/search?cvredirect=2&suggest_reqid=91938777584344923039168083875807&text=слон'}]
    else:
        user_answ = req['resquest']['command']
        res['response']['text'] = f'Все гвороят {user_answ}, а ты купи кролика'
        res['response']['buttons'] = [{'title': choice(['ладно', 'куплю', 'покупаю', 'хорошо'])}]


@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


if __name__ == '__main__':
    app.run()
