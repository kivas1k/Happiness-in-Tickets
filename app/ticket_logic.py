def read_and_analyze_tickets(file_path):
    """
    Функция для считывания и анализа билетов.
    Возвращает список всех билетов и список счастливых билетов.
    """
    try:
        with open(file_path, 'r') as file:
            tickets = file.readlines()
        tickets = [ticket.strip() for ticket in tickets if ticket.strip()]
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return [], []

    lucky_tickets = [ticket for ticket in tickets if is_lucky(ticket)]
    return tickets, lucky_tickets


def is_lucky(ticket):
    """
    Функция для проверки, является ли билет счастливым.
    Счастливым считается билет с шестизначным номером, у которого сумма первых трёх цифр равна сумме последних.
    """
    ticket_str = str(ticket)
    if len(ticket_str) == 6:
        first_half = sum(int(digit) for digit in ticket_str[:3])
        second_half = sum(int(digit) for digit in ticket_str[3:])
        return first_half == second_half
    return False


def count_even_odd_tickets(tickets):
    """
    Функция для подсчета четных и нечетных билетов.

    Логика:
      1. Перебираем все билеты и пытаемся преобразовать их в число.
      2. Если преобразование успешно, добавляем число в список valid_numbers.
      3. Подсчитываем количество четных чисел через генератор, а нечетных – как разницу между общим количеством и числом четных.
    """
    valid_numbers = []
    for ticket in tickets:
        try:
            number = int(ticket)
            valid_numbers.append(number)
        except ValueError:
            continue
    even_count = sum(1 for num in valid_numbers if num % 2 == 0)
    odd_count = len(valid_numbers) - even_count
    return even_count, odd_count


def count_lucky_tickets(tickets):
    """
    Функция для подсчета счастливых билетов.
    """
    return sum(1 for ticket in tickets if is_lucky(ticket))
