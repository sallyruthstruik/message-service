import requests

from flaskapp import app
from sender.celery_app import celery_logger


class Telegram(object):
    """Класс транспорта Telegram сообщений

    """

    @staticmethod
    def send(message):
        """Метод отправки сообщения

        :param message:
        :return: результат отправки
        """
        data = {"text": message.body}
        result = True
        celery_logger.info("Отправка сообщения %s адресату %s" % (message.id, message.recipient))

        data.update({"chat_id": message.recipient})
        r = requests.post("https://api.telegram.org/bot%s/sendMessage" % app.config["TELEGRAM_BOT_TOKEN"], json=data)
        if r.status_code == 200:
            celery_logger.info("Сообщение %s отправлено адресату %s" % (message.id, message.recipient))
        else:
            #review
            celery_logger.exception("Произошла ошибка при отправке сообщения %s адресату %s: %s:%s",
                                    message.id,
                                    message.recipient,
                                    r.status_code, r.text)
            result = False
        return result
