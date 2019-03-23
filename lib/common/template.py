from lib.common.messaging import Messages


class Templates:

    def __init__(self, file: str):
        self.file = file

    def read(self):
        return Messages.load(self.file)


# Commands Messages
START_MESSAGE = HELP_MESSAGE = Templates("commands/help.md")
GROUP_LINK = Templates("commands/group_link.md")
GROUP_LINK_DISABLED = Templates("commands/group_link_disabled.md")
SMART_QUESTION_LINK = Templates("commands/smart_question_link.md")
TOR_INSTALLATION_LINK = Templates("commands/tor_installation_link.md")
FARSI = Templates("commands/farsi.md")
KALI = Templates("commands/kali.md")
GRUB_REPAIR = Templates("commands/grub_repair.md")
ASK_QUESTION = Templates("commands/ask_question.md")
ABOUT = Templates("commands/about.md")
IT_IS_SUPERGROUP_COMMAND = Templates('it_is_supergroup_command.md')
USAGE = Templates('usage.md')

# Triggers Messages
WELCOME = Templates("welcome.md")
REGISTRATION_ACCEPTED = Templates("registration_accepted.md")
JUST_TAGGED_USER = Templates("just_tagged_user.md")
REGISTRATION_VERIFY_BUTTON = Templates("registration_verify_button.md")
REPORT_MESSAGE = Templates("report/report_message.md")
DELETE_REPORTED_MESSAGE_BUTTON = Templates("report/delete_reported_message_button.md")
DELETE_REPORTED_MESSAGE = Templates('report/delete_reported_message_notification.md')
