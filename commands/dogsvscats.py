import urllib.request
import os

from logic_application.neural_network import NeuralModel
import command_system


def download_attachments(attachments):
    for i in range(len(attachments)):
        urllib.request.urlretrieve(attachments[i], f"images/detect-{i}.jpg")
    files = list(filter(lambda i: 'detect' in i, os.listdir('images/')))
    files = sorted(files, key=lambda x: x.split('-')[1])
    return files, NeuralModel.convert_images(files)


def detect(attachments):
    model = NeuralModel()
    n_files = len(attachments)
    message = ""
    files, images = download_attachments(attachments)
    model.load_model()
    for i in range(n_files):
        response = model.predict(images[i], files[i])
        message += f"на картинке {i+1}/{n_files}. {response['answer']['answer']}\n"
    return message, ""


detect_command = command_system.Command()

detect_command.keys = ["$"]
detect_command.get_content = True
detect_command.description = "Отправь фото и я распознаю на нем я распознаю на нем кота или собаку"
detect_command.process = detect
