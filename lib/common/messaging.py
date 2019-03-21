from lib.common.services import log
from lib.loader import template_loader


class Messages:
    NOT_EXISTS = "فایل مورد نظر وجود ندارد"
    SUPPORT = "لطفا به پشتیبانی اطلاع دهید"

    @staticmethod
    def load(file: str) -> str:
        content = template_loader(file)
        if content is None:
            log.error(__file__, "load", Messages.NOT_EXISTS)
            return Messages.SUPPORT
        return content.strip()

