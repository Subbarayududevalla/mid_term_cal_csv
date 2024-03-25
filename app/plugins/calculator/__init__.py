import logging
import os
from app.commands import Command
import pandas as pd
from datetime import datetime

class CalculatorCommand(Command):
    """
    A command-line calculator that performs basic arithmetic operations 
    and stores the history in a pandas DataFrame. Supports configuration 
    via environment variables for base path and logging level.
    """

    def __init__(self):
        self.calculator = Calculator()
        self.base_path = os.getenv('CALCULATOR_BASE_PATH', '.')  # Use environment variable for base path
        self.logging_level = getattr(logging, os.getenv('CALCULATOR_LOG_LEVEL', 'INFO'))  # Use environment variable for logging level
        logging.basicConfig(level=self.logging_level)  # Configure logging

    def execute(self):
        """Starts the calculator REPL, prompting for user input and performing calculations."""
        while True:
            user_input = input("Enter operation (+, -, *, /, or exit): ").strip()

            if user_input == "exit":
                self.save_history()
                break

            try:
                result = self.calculator.calculate(user_input)
                print(f"Result: {result}")
            except (ValueError, ZeroDivisionError) as e:
                logging.error(f"Error: {e}")  # Log errors
                print(f"Error: {str(e)}")  # User-friendly error message

    def save_history(self):
        """Saves the calculator history to a CSV file."""
        timestamp = datetime.now().strftime("%d%m%y%H%M%S")
        filename = f"calculator_history_{timestamp}.csv"

        # Create "csv_history" folder if it doesn't exist
        folder_path = os.path.join(self.base_path, "csv_history")  # Use base path for flexibility
        os.makedirs(folder_path, exist_ok=True)

        # Save history to CSV in "csv_history" folder
        self.calculator.history_df.to_csv(os.path.join(folder_path, filename), index=False)
        logging.info(f"Calculator history saved to {os.path.join(folder_path, filename)}")  # Log successful save

class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations 
    and stores the history in a pandas DataFrame.
    """

    def __init__(self):
        """
        Initializes the calculator with an empty DataFrame for history.
        """
        self.history_df = pd.DataFrame(columns=[ "operand1", "operation","operand2", "result"])

    def calculate(self, user_input):
        """
        Performs a calculation based on the user input and adds it to the history.

        Args:
            user_input (str): The user's expression (e.g., "2 + 3").

        Returns:
            float: The result of the calculation, or None if a history-only operation is given.

        Raises:
            ValueError: If the input format is invalid or an invalid operation is entered.
            ZeroDivisionError: If division by zero is attempted.
        """
        expression = user_input.strip().split()

        # Handle history-only operations
        if len(expression) == 1 and expression[0] in ("history", "exit"):
            return None  # Indicate no calculation result

        if len(expression) != 3:
            raise ValueError("Invalid expression format. Please enter a valid operation with operands.")

        try:
            # Convert operands to float, removing any leading/trailing spaces
            operand1 = float(expression[0].strip())
            operand2 = float(expression[2].strip())

            if expression[1] == "+":
                result = operand1 + operand2
            elif expression[1] == "-":
                result = operand1 - operand2
            elif expression[1] == "*":
                result = operand1 * operand2
            elif expression[1] == "/":
                result = operand1 / operand2
            else:
                raise ValueError("Invalid operation.")

            # Save calculation to DataFrame
            self.history_df = self.history_df._append({
                "operand1": operand1,
                "operation": expression[1],
                "operand2": operand2,
                "result": result
            }, ignore_index=True)

            return result
        except ZeroDivisionError:
            raise  # Re-raise ZeroDivisionError for handling
        except ValueError:
            logging.error(f"Error: Invalid number format. Please enter valid numbers.")
            raise  # Re-raise ValueError for user-friendly message

