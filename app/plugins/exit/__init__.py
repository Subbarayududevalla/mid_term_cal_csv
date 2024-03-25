import logging
from app.commands import Command


class ExitCommand(Command):
    def execute(self):
        logging.info("Thanks, See you again")
        print("Thanks, See you again :)")