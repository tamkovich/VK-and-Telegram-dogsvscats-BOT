import importlib
import os

from logic_application.telegramapi import Telegram
from logic_application.vkapi import Vk
from command_system import command_list


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]


def load_modules():
    files = os.listdir("commands")
    modules = filter(lambda x: x.endswith(".py"), files)
    for m in modules:
        importlib.import_module("commands." + m[0:-3])


def get_answer(action, content=None):
    message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
    attachment = ""
    distance = len(action)
    command = None
    key = ""
    file = None
    for c in command_list:
        for k in c.keys:
            d = damerau_levenshtein_distance(action, k)
            if d < distance:
                distance = d
                command = c
                key = k
                if distance == 0:
                    if c.return_content or c.get_content:
                        if c.file:
                            message, attachment, file = c.process(content)
                        else:
                            message, attachment = c.process(content)
                    else:
                        if c.file:
                            message, attachment, file = c.process()
                        else:
                            message, attachment = c.process()
                    return message, attachment, file
    if distance < len(action) * 0.4:
        if command.file:
            message, attachment, file = command.process()
        else:
            message, attachment = command.process()
        message = f'Я понял ваш запрос как "{key}"\n\n' + message
    return message, attachment, file


def create_answer(data, token, messanger=None):
    load_modules()
    if messanger == 0:
        create_answer_vk(data, token)
    elif messanger == 1:
        create_answer_tg(data, token)


def _action_detect(action, data_text):
    text = None
    if action.startswith('/'):
        action = action.split(' ')[0]
        text = data_text[len(action):].strip()
    return action, text


def create_answer_vk(data, token):
    vk = Vk(token=token)
    user_id = data["user_id"]
    action = data["body"]
    attachments = data.get('attachments')

    # распознование команд
    action, text = _action_detect(action, data["body"])
    # распознование фото
    if attachments:
        action = '$'
        text = list(map(lambda p: p['photo']['photo_604'], attachments))
    elif action == '$':
        action = 'помощь'

    message, attachment, file = get_answer(action.lower(), text)
    vk.send_message(user_id, message, attachment, file)


def create_answer_tg(data, token):
    tg = Telegram(token)
    user_id = data["chat"]["id"]
    action = data.get("text", '')
    attachments = data.get('photo')

    # распознование команд
    action, text = _action_detect(action, action)
    # распознование фото
    if attachments:
        action = '$'
        text = [tg.get_file_url(attachments[-1]['file_id'])]
    elif action == '$':
        action = 'помощь'

    message, attachment, file = get_answer(action.lower(), text)
    tg.send_message(user_id, message, attachment, file)
