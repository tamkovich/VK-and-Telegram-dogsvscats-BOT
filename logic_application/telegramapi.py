import telebot


class Telegram:

    FILE_URL = "https://api.telegram.org/file/bot{0}/{1}"

    def __init__(self, token=None):
        self.token = token
        self.api = telebot.TeleBot(token=token)

    def get_file_path(self, file_id):
        return self.api.get_file(file_id).file_path

    def get_file_url(self, file_id):
        return self.FILE_URL.format(self.token, self.get_file_path(file_id))

    def send_message(self, user_id, message, attachment="", file=None):
        if not self.api.token:
            self.api.token = self.token
        if file:
            file = self.api.get_file(file)
            self._send_photo(user_id, message, file)
        else:
            self.api.send_chat_action(user_id, 'typing')
            self.api.send_message(user_id, message)

    def _send_photo(self, user_id, message, file):
        self.api.send_chat_action(user_id, 'file load')
        openedfile = open(file, "rb")
        files = {"file": openedfile}
        self.api.send_photo(user_id, files['file'], caption=message)
        openedfile.close()
