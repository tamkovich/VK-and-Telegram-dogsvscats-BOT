import requests
import json
import vk


class Vk:

    def __init__(self, token):
        self.token = token
        session = vk.Session()
        self.api = vk.API(session, v=5.0)

    def send_message(self, user_id, message, attachment="", file=None):
        if file:
            self._send_photo(user_id, message, file)
        else:
            self.api.messages.send(
                access_token=self.token,
                user_id=str(user_id),
                message=message,
                attachment=attachment,
            )

    def _send_photo(self, user_id, message, file):
        openedfile = open(file, "rb")
        files = {"file": openedfile}
        fileonserver = json.loads(
            requests.post(
                self.api.photos.getMessagesUploadServer(access_token=self.token)["upload_url"],
                files=files,
            ).text
        )
        attachment = self.api.photos.saveMessagesPhoto(
            access_token=self.token,
            server=fileonserver["server"],
            photo=fileonserver["photo"],
            hash=fileonserver["hash"],
        )
        attachment = f'photo{attachment[0]["owner_id"]}_{attachment[0]["id"]}'
        if message:
            self.api.messages.send(
                access_token=self.token, user_id=user_id, message=message, attachment=attachment
            )
        else:
            self.api.messages.send(access_token=self.token, user_id=user_id, attachment=attachment)
        openedfile.close()
