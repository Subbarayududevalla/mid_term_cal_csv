import pytest
from app.plugins.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture to provide a Calculator instance."""
    return Calculator()


def test_addition(calculator: Calculator):
    """Tests addition operation."""
    result = calculator.calculate("2 + 3")
    assert result == 5, "Addition failed"


def test_subtraction(calculator: Calculator):
    """Tests subtraction operation."""
    result = calculator.calculate("4 - 1")
    assert result == 3, "Subtraction failed"


def test_multiplication(calculator: Calculator):
    """Tests multiplication operation."""
    result = calculator.calculate("2 * 5")
    assert result == 10, "Multiplication failed"


def test_division(calculator: Calculator):
    """Tests division operation."""
    result = calculator.calculate("6 / 2")
    assert result == 3, "Division failed"


def test_division_by_zero(calculator: Calculator):
    """Tests division by zero."""
    with pytest.raises(ZeroDivisionError):
        calculator.calculate("10 / 0")


def test_invalid_expression(calculator: Calculator):
    """Tests invalid expression format."""
    with pytest.raises(ValueError):
        calculator.calculate("invalid expression")


def test_missing_operands(calculator: Calculator):
    """Tests expressions with missing operands."""
    with pytest.raises(ValueError):
        calculator.calculate("+")
    with pytest.raises(ValueError):
        calculator.calculate("2 +")


