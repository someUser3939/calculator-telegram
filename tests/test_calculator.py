import math  # Проверяем, что результат вычисления остаётся конечным.
import unittest  # Используем стандартный тестовый фреймворк Python.

from logic.calculator import calculate, parse_number  # Импортируем логику, которую проверяют тесты.


class ParseNumberTests(unittest.TestCase):  # Проверяем преобразование вводимых чисел.
    def test_parses_dot_and_comma_decimal_separators(self) -> None:  # Убеждаемся в поддержке обоих разделителей дроби.
        self.assertEqual(parse_number(" 3.5 "), 3.5)  # Проверяем пробелы вокруг числа и десятичную точку.
        self.assertEqual(parse_number("3,5"), 3.5)  # Проверяем десятичную запятую.

    def test_rejects_non_numbers_and_non_finite_values(self) -> None:  # Проверяем обработку некорректных чисел.
        for text in ("abc", "", "nan", "inf"):  # Перебираем нечисловое значение, пустую строку и бесконечность.
            with self.subTest(text=text):  # Показываем конкретное значение при неудаче теста.
                with self.assertRaises(ValueError):  # Ожидаем ошибку разбора каждого такого значения.
                    parse_number(text)  # Запускаем разбор проверяемого текста.


class CalculateTests(unittest.TestCase):  # Проверяем арифметические операции.
    def test_calculates_supported_operations(self) -> None:  # Проверяем правильность всех допустимых операций.
        self.assertEqual(calculate(7, 2, "+"), 9)  # Проверяем сложение.
        self.assertEqual(calculate(7, 2, "-"), 5)  # Проверяем вычитание.
        self.assertEqual(calculate(7, 2, "*"), 14)  # Проверяем умножение.
        self.assertEqual(calculate(7, 2, "/"), 3.5)  # Проверяем деление.

    def test_rejects_division_by_zero(self) -> None:  # Проверяем запрет деления на ноль.
        with self.assertRaises(ZeroDivisionError):  # Ожидаем специальное исключение деления на ноль.
            calculate(7, 0, "/")  # Выполняем деление на ноль для проверки ошибки.

    def test_rejects_unknown_operation(self) -> None:  # Проверяем реакцию на неизвестный знак.
        with self.assertRaises(ValueError):  # Ожидаем ошибку неподдерживаемой операции.
            calculate(7, 2, "%")  # Передаём намеренно неразрешённый знак процента.

    def test_rejects_non_finite_result(self) -> None:  # Проверяем обработку переполнения вычисления.
        with self.assertRaises(OverflowError):  # Ожидаем исключение для слишком большого результата.
            calculate(float.fromhex("0x1.fffffffffffffp+1023"), 2, "*")  # Перемножаем максимальное конечное значение и два.
        self.assertTrue(math.isfinite(calculate(2, 3, "+")))  # Дополнительно убеждаемся в конечности обычного ответа.


if __name__ == "__main__":  # Позволяем запускать тестовый файл напрямую.
    unittest.main()  # Запускаем тесты стандартным unittest-раннером.
