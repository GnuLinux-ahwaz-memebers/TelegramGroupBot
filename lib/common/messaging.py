from lib.loader import template_loader


class Messages:
    NOT_EXISTS = "فایل مورد نظر وجود ندارد"

    @staticmethod
    def load(file: str) -> str:
        content = template_loader(file)
        if content is None:
            return Messages.NOT_EXISTS
        return content


class Templates:
    START_MESSAGE = HELP_MESSAGE = "help.md"
    WELCOME = "welcome.md"
    REGISTRATION_ACCEPTED = "registration_accepted.md"
    JUST_TAGGED_USER = "just_tagged_user.md"
    REGISTRATION_VERIFY_BUTTON = "registration_verify_button.md"
