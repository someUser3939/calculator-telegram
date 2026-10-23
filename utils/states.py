from aiogram.fsm.state import State, StatesGroup  # Импортируем типы состояний конечного автомата aiogram.


class CalculatorForm(StatesGroup):  # Описываем шаги пользовательского расчёта.
    number_1 = State()  # Ожидаем первое число.
    number_2 = State()  # Ожидаем второе число.
    operation = State()  # Ожидаем знак арифметической операции.
