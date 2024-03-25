from abc import ABC, abstractmethod
from decimal import Decimal

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_name: str | Decimal):
        """Handle both decimal and string command names."""
        try:
            self.commands[command_name].execute()  # Attempt to convert and use string representation
        except (KeyError, TypeError):
            print(f"No such command: {command_name}")