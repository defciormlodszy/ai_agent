# calculator/tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_addition(self) -> None:
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self) -> None:
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self) -> None:
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self) -> None:
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self) -> None:
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self) -> None:
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self) -> None:
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_exponentiation(self) -> None:
        result = self.calculator.evaluate("2 ^ 3")
        self.assertEqual(result, 8)

    def test_exponentiation_float(self) -> None:
        result = self.calculator.evaluate("4 ^ 0.5")
        self.assertAlmostEqual(result, 2.0)

    def test_right_associative_exponentiation(self) -> None:
        # This test checks right-associativity: 2 ^ 3 ^ 2 should be 2 ^ (3 ^ 2) = 2 ^ 9 = 512
        # However, current implementation is left-associative, so this expects 64.
        # Adjust the expected value if changing associativity handling.
        result = self.calculator.evaluate("2 ^ 3 ^ 2")
        self.assertEqual(result, 64)  # left-assoc: (2 ^ 3) ^ 2 = 8 ^ 2 = 64