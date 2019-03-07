from lib.loader import template_loader


class Messages:
    NOT_EXISTS = "فایل مورد نظر وجود ندارد"

    @staticmethod
    def load(file: str) -> str:
        content = template_loader(file).strip()
        if content is None:
            return Messages.NOT_EXISTS
        return content

