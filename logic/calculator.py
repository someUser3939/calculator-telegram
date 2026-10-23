import math  # Проверяем, что числа и ответы конечны.


def parse_number(text: str) -> float:  # Преобразуем пользовательский текст в число.
    try:  # Перехватываем ошибку преобразования нечислового ввода.
        number = float(text.strip().replace(",", "."))  # Поддерживаем точку и запятую как десятичный разделитель.
    except ValueError as error:  # Обрабатываем текст, который не является числом.
        raise ValueError("Please enter a valid number.") from error  # Передаём вызывающему коду понятную ошибку.

    if not math.isfinite(number):  # Запрещаем NaN и бесконечности.
        raise ValueError("The number must be finite.")  # Возвращаем ошибку для некорректных математических значений.
    return number  # Возвращаем проверенное число.


def calculate(number_1: float, number_2: float, operation: str) -> float:  # Вычисляем результат выбранной операции.
    if operation == "+":  # Выбираем сложение.
        result = number_1 + number_2  # Складываем два числа.
    elif operation == "-":  # Выбираем вычитание.
        result = number_1 - number_2  # Вычитаем второе число из первого.
    elif operation == "*":  # Выбираем умножение.
        result = number_1 * number_2  # Перемножаем два числа.
    elif operation == "/":  # Выбираем деление.
        if number_2 == 0:  # Не допускаем деление на ноль.
            raise ZeroDivisionError("Division by zero is not allowed.")  # Возвращаем вызывающему коду отдельный тип ошибки.
        result = number_1 / number_2  # Делим первое число на второе.
    else:  # Обрабатываем знак, который не поддерживает калькулятор.
        raise ValueError(f"Unsupported operation: {operation}")  # Явно сообщаем о неизвестной операции.

    if not math.isfinite(result):  # Проверяем результат на переполнение.
        raise OverflowError("The result is too large.")  # Не возвращаем бесконечное значение.
    return result  # Возвращаем конечный результат вычисления.
