import pandas as pd

def read_and_analyze_tickets(file_path):
    """
    Функция для считывания и анализа билетов.
    Возвращает все билеты и счастливые билеты.
    """
    try:
        with open(file_path, 'r') as file:
            tickets = file.readlines()
        tickets = [ticket.strip() for ticket in tickets if ticket.strip()]
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return [], []

    # Разделяю билеты на счастливые и обычные
    lucky_tickets = [ticket for ticket in tickets if is_lucky(ticket)]  # Фильтрую счастливые билеты
    return tickets, lucky_tickets  # Возвращаю все билеты и счастливые билеты


def is_lucky(ticket):
    """
    Функция для проверки, является ли билет счастливым.
    Счастливый билет, если сумма первых 3 цифр равна сумме последних 3.
    """
    ticket_str = str(ticket)  # Преобразую номер билета в строку
    if len(ticket_str) == 6:
        first_half = sum(int(digit) for digit in ticket_str[:3])
        second_half = sum(int(digit) for digit in ticket_str[3:])
        return first_half == second_half
    return False  # Если длина билета не 6 или суммы не равны, билет не счастливый
