from threading import Thread

import requests
import os

from lib.commands.helper import messageRemover, group_command
from lib.common.services import log
from tempfile import gettempdir
# TODO: Handling  worker threads using PoolExecuter doesn't work :|
# from concurrent.futures import ThreadPoolExecutor as PoolExecutor
# Constants
from lib.loader import Config

# executor = PoolExecutor(3)
# executor = ThreadPoolExecutor(Config.getInt("GENERAL.MAX_THREAD_COUNT", 3)))

API_URL = "https://api.deepai.org/api/nsfw-detector"


def detect_nudity_deepai_api(image_path: str, api_key: str = None) -> int:
    if api_key is None:
        api_key = Config.get("NUDITY_DETECTION.API_KEY", None)
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


def download_image_async(bot, update, file_id):
    bot_file = bot.getFile(file_id=file_id)
    image_location = os.path.join(gettempdir(), file_id)
    bot_file.download(image_location)
    try:
        # pass image to check nudity (thread)
        accuracy = detect_nudity_deepai_api(image_location)
        # decision delete message or not
        if accuracy >= Config.getFloat("NUDITY_DETECTION.ACCURACY_THRESHHOLD"):
            messageRemover(bot, update.message)
    except Exception as e:
        log.error(__file__, 'download_image_async', e)

    # remove downloaded image if found
    if os.path.exists(image_location):
        os.remove(image_location)


@group_command
def handler(bot, update):
    # download images in
    # image_dl_threads = []
    # for photo in update.message.photo:
    #     file_id = photo.file_id
    file_id = update.message.photo[-1].file_id
    download_file_thread = Thread(target=download_image_async, args=(bot, update, file_id))
    download_file_thread.start()
    log.info("Downloading image {} async".format(file_id))
    # executor.submit(download_image_async, bot, update, file_id)
    # download_image_async(bot, update, file_id)
    # image_dl_threads.append(image_dl_thread)
    # image_dl_thread.join()
