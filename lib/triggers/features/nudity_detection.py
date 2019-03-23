import requests
import os

from lib.commands.helper import messageRemover, group_command
from lib.common.services import log

# Constants
from lib.loader import Config

API_URL = "https://api.deepai.org/api/nsfw-detector"


def detection(image_path: str, api_key: str = None) -> int:
    if api_key is None:
        api_key = Config().get("features.NUDITY_DETECTION.API_KEY", None)
    try:
        req = requests.post(
            API_URL,
            files={
                'image': open(image_path, 'rb'),
            },
            headers={'api-key': api_key}
        )

        if str(req.status_code) == "200":
            return req.json().get('output', {}).get('nsfw_score', 0)
    except Exception as e:
        log.error(__file__, "nudity_detection", e)
    return 0


@group_command
def handler(bot, update):
    # download image
    file_id = update.message.photo[-1].file_id
    file = bot.getFile(file_id=file_id)
    # TODO: i have any idea about windows systems for this location =)
    image_location = "/tmp/{}.jpg".format(file_id)
    file.download(image_location)

    # TODO: it's better to use safe-thread
    # pass image to check nudity (thread)
    accuracy = detection(image_location)

    # decision delete message or not
    if accuracy >= Config().get("features.NUDITY_DETECTION.ACCURACY"):
        messageRemover(bot, update.message)

    # remove downloaded image
    os.remove(image_location)
