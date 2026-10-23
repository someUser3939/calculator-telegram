from aiogram import F, Router  # Импортируем фильтры сообщений и роутер aiogram.
from aiogram.filters import Command, CommandStart  # Импортируем фильтры команд бота.
from aiogram.fsm.context import FSMContext  # Импортируем доступ к состоянию диалога.
from aiogram.types import Message  # Импортируем тип сообщения Telegram.

from logic.calculator import calculate, parse_number  # Подключаем функции разбора числа и вычисления.
from utils.states import CalculatorForm  # Подключаем состояния шагов калькулятора.

router = Router()  # Создаём роутер для пользовательских команд.


@router.message(CommandStart())  # Вызываем обработчик по команде /start.
async def cmd_start(message: Message, state: FSMContext) -> None:  # Начинаем новый расчёт.
    await state.clear()  # Удаляем данные предыдущего расчёта.
    await state.set_state(CalculatorForm.number_1)  # Ожидаем ввода первого числа.
    await message.answer("Привет! Я калькулятор. Введите первое число:")  # Отправляем первое приглашение.


@router.message(Command("cancel"))  # Обрабатываем команду отмены.
async def cmd_cancel(message: Message, state: FSMContext) -> None:  # Завершаем текущий диалог.
    await state.clear()  # Очищаем активное состояние пользователя.
    await message.answer("Расчёт отменён. Чтобы начать заново, отправьте /start.")  # Объясняем, как начать снова.


@router.message(CalculatorForm.number_1)  # Принимаем ответ на приглашение ввести первое число.
async def process_number_1(message: Message, state: FSMContext) -> None:  # Проверяем и сохраняем первое число.
    if message.text is None:  # Проверяем, что сообщение содержит текст.
        await message.answer("Нужно ввести число текстом. Попробуйте ещё раз:")  # Просим отправить числовой текст.
        return  # Остаёмся на текущем шаге диалога.

    try:  # Пробуем преобразовать введённый текст в конечное число.
        number_1 = parse_number(message.text)  # Разбираем целое или десятичное значение.
    except ValueError:  # Обрабатываем некорректное числовое значение.
        await message.answer("Не удалось распознать число. Введите, например, 12 или 3.5:")  # Просим повторить ввод.
        return  # Не переключаемся на следующий шаг до правильного ввода.

    await state.update_data(number_1=number_1)  # Сохраняем первое число в FSM.
    await state.set_state(CalculatorForm.number_2)  # Переключаем пользователя на ввод второго числа.
    await message.answer("Введите второе число:")  # Просим ввести второе число.


@router.message(CalculatorForm.number_2)  # Принимаем ответ на приглашение ввести второе число.
async def process_number_2(message: Message, state: FSMContext) -> None:  # Проверяем и сохраняем второе число.
    if message.text is None:  # Проверяем, что сообщение содержит текст.
        await message.answer("Нужно ввести число текстом. Попробуйте ещё раз:")  # Просим отправить числовой текст.
        return  # Остаёмся на текущем шаге диалога.

    try:  # Пробуем преобразовать введённый текст в конечное число.
        number_2 = parse_number(message.text)  # Разбираем целое или десятичное значение.
    except ValueError:  # Обрабатываем некорректное числовое значение.
        await message.answer("Не удалось распознать число. Введите, например, 12 или 3.5:")  # Просим повторить ввод.
        return  # Не переключаемся на следующий шаг до правильного ввода.

    await state.update_data(number_2=number_2)  # Сохраняем второе число в FSM.
    await state.set_state(CalculatorForm.operation)  # Переключаем пользователя на выбор операции.
    await message.answer("Выберите операцию: +, -, * или /")  # Показываем допустимые знаки.


@router.message(CalculatorForm.operation, F.text.in_({"+", "-", "*", "/"}))  # Пропускаем только известные операции.
async def process_operation(message: Message, state: FSMContext) -> None:  # Вычисляем и отправляем результат.
    data = await state.get_data()  # Получаем сохранённые числа текущего пользователя.
    number_1 = data.get("number_1")  # Читаем первое сохранённое число.
    number_2 = data.get("number_2")  # Читаем второе сохранённое число.
    operation = message.text  # Сохраняем полученный знак операции.

    if operation not in {"+", "-", "*", "/"}:  # Дополнительно проверяем знак операции.
        await message.answer("Неизвестная операция. Выберите: +, -, * или /")  # Просим выбрать допустимый знак.
        return  # Не выполняем расчёт для неподдерживаемой операции.

    if not isinstance(number_1, (int, float)) or not isinstance(number_2, (int, float)):  # Проверяем целостность FSM-данных.
        await state.clear()  # Удаляем некорректное состояние расчёта.
        await message.answer("Данные расчёта потеряны. Отправьте /start, чтобы начать заново.")  # Объясняем, как восстановиться.
        return  # Останавливаем расчёт без обоих чисел.

    try:  # Запускаем арифметическую операцию.
        result = calculate(number_1, number_2, operation)  # Вычисляем результат в модуле бизнес-логики.
    except ZeroDivisionError:  # Обрабатываем попытку деления на ноль.
        await state.clear()  # Завершаем неудачный расчёт и очищаем сохранённые числа.
        await message.answer("На ноль делить нельзя. Отправьте /start, чтобы начать новый расчёт.")  # Сообщаем о причине ошибки.
        return  # Не отправляем несуществующий результат.
    except OverflowError:  # Обрабатываем слишком большой результат.
        await state.clear()  # Сбрасываем состояние завершённого неудачного расчёта.
        await message.answer("Результат слишком велик. Отправьте /start, чтобы начать новый расчёт.")  # Предлагаем повторить расчёт.
        return  # Не отправляем бесконечное или некорректное значение.

    await state.clear()  # Очищаем состояние после завершённого вычисления.
    await message.answer(f"Результат: {number_1:g} {operation} {number_2:g} = {result:g}")  # Показываем пользователю выражение и ответ.


@router.message(CalculatorForm.operation)  # Ловим неподдерживаемый ввод на этапе выбора операции.
async def process_invalid_operation(message: Message) -> None:  # Подсказываем допустимые знаки.
    await message.answer("Неизвестная операция. Выберите: +, -, * или /")  # Просим пользователя повторить выбор.
