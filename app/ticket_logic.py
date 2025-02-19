import numpy as np
from sympy import isprime, integer_nthroot

def read_and_analyze_tickets(file_path):
    """
    Функция для считывания и анализа билетов.
    """
    try:
        with open(file_path, 'r') as file:
            tickets = file.readlines()
        tickets = np.array([ticket.strip() for ticket in tickets if ticket.strip()])
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return np.array([]), np.array([])

    lucky_tickets = tickets[np.vectorize(is_lucky)(tickets)]
    return tickets, lucky_tickets

def is_lucky(ticket):
    """Проверяет, является ли билет счастливым."""
    ticket_str = str(ticket)
    if len(ticket_str) == 6 and ticket_str.isdigit():
        digits = np.array(list(map(int, ticket_str)))
        return digits[:3].sum() == digits[3:].sum()
    return False

def count_even_odd_tickets(tickets):
    """Подсчитывает четные и нечетные билеты."""
    try:
        numbers = np.array(list(map(int, tickets)))
        even_count = np.sum(numbers % 2 == 0)
        return even_count, len(numbers) - even_count
    except ValueError:
        return 0, 0

def count_lucky_tickets(tickets):
    """Подсчитывает количество счастливых билетов."""
    return np.sum(np.vectorize(is_lucky)(tickets))

def is_palindrome(ticket):
    """Проверяет, является ли билет палиндромом."""
    ticket_str = str(ticket)
    return ticket_str == ticket_str[::-1] if ticket_str.isdigit() and len(ticket_str) == 6 else False

def count_palindromic_tickets(tickets):
    """Подсчитывает количество палиндромных билетов."""
    return np.sum(np.vectorize(is_palindrome)(tickets))

def count_prime_tickets(tickets):
    """Подсчитывает количество билетов, являющихся простыми числами."""
    try:
        numbers = np.array(list(map(int, tickets)))
        return np.sum(np.vectorize(isprime)(numbers))
    except ValueError:
        return 0

def count_divisible_tickets(tickets):
    """Подсчитывает количество билетов, у которых одна половина делится на другую."""
    count = 0
    for ticket in tickets:
        ticket_str = str(ticket)
        if len(ticket_str) == 6 and ticket_str.isdigit():
            left, right = int(ticket_str[:3]), int(ticket_str[3:])
            if (left != 0 and right % left == 0) or (right != 0 and left % right == 0):
                count += 1
    return count


def is_square(ticket):
    """Проверяет, является ли номер билета квадратом числа."""
    try:
        ticket_num = int(ticket)
        root, is_exact = integer_nthroot(ticket_num, 2)
        return is_exact
    except ValueError:
        return False

def is_cube(ticket):
    """Проверяет, является ли номер билета кубом числа."""
    try:
        ticket_num = int(ticket)
        root, is_exact = integer_nthroot(ticket_num, 3)
        return is_exact
    except ValueError:
        return False

def is_nth_power(ticket, n):
    """Проверяет, является ли номер билета n-ой степенью числа."""
    try:
        ticket_num = int(ticket)
        if n <= 0:
            return False
        root, is_exact = integer_nthroot(ticket_num, n)
        return is_exact
    except ValueError:
        return False

def find_lucky_ticket_intervals(lucky_tickets):
    """
    Находит самый короткий и самый длинный промежуток между всеми возможными парами счастливых билетов.
    """
    if len(lucky_tickets) < 2:
        return None, None

    lucky_numbers = np.array(list(map(int, lucky_tickets)))

    all_differences = np.abs(lucky_numbers[:, None] - lucky_numbers)

    min_interval = np.min(all_differences[all_differences > 0])
    max_interval = np.max(all_differences)

    return min_interval, max_interval


def calculate_lucky_density(tickets):
    ticket_numbers = []
    for ticket in tickets:
        padded_ticket = str(ticket).zfill(6)
        if len(padded_ticket) != 6:
            continue
        try:
            num = int(padded_ticket)
            ticket_numbers.append(num)
        except ValueError:
            continue

    if not ticket_numbers:
        return np.array([]), np.array([]), np.array([])

    # Фиксируем диапазон от 000000 до 1000000
    min_ticket = 0
    max_ticket = 1000000
    num_bins = 10
    bin_edges = np.linspace(min_ticket, max_ticket, num_bins + 1)

    # Гистограмма для всех билетов
    hist_all, _ = np.histogram(ticket_numbers, bins=bin_edges)

    # Гистограмма для счастливых билетов
    lucky_numbers = [int(str(t).zfill(6)) for t in tickets if is_lucky(t)]
    hist_lucky, _ = np.histogram(lucky_numbers, bins=bin_edges)

    # Расчет плотности
    density = np.divide(hist_lucky, hist_all, out=np.zeros_like(hist_lucky, dtype=float), where=hist_all != 0)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    return bin_centers, density, bin_edges
