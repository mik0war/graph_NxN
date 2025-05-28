import matplotlib.pyplot as plt
from matplotlib import rcParams


def display_matrix_with_greek(matrix, matrix_type="pmatrix", font_size=16, dpi=100):
    """
    Визуализирует матрицу с поддержкой греческих символов без использования LaTeX

    Параметры:
        matrix (list of lists): Матрица в виде списка списков
        matrix_type (str): Тип окружения для матрицы:
            "pmatrix" - круглые скобки (по умолчанию)
            "bmatrix" - квадратные скобки
            "vmatrix" - вертикальные черты
        font_size (int): Размер шрифта
        dpi (int): Качество изображения
    """
    # Отключаем LaTeX-рендеринг
    rcParams['text.usetex'] = False

    # Генерация текстового представления матрицы
    matrix_text = generate_matrix_text(matrix, matrix_type)

    # Создание изображения
    fig = plt.figure(figsize=(len(matrix[0]) / 2 + 1, len(matrix) / 2 + 1), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Отображение матрицы
    ax.text(0.5, 0.5, matrix_text,
            fontsize=font_size,
            ha='center',
            va='center',
            fontfamily='serif')

    plt.show()


def generate_matrix_text(matrix, matrix_type):
    """
    Генерирует текстовое представление матрицы с греческими символами
    """
    if not matrix:
        return ""

    # Определяем символы скобок
    brackets = {
        "pmatrix": ("(", ")"),
        "bmatrix": ("[", "]"),
        "vmatrix": ("|", "|"),
        "matrix": ("", "")
    }

    left_bracket, right_bracket = brackets.get(matrix_type, ("(", ")"))

    # Собираем строки матрицы
    rows = []
    for row in matrix:
        row_str = "  ".join(str(item) for item in row)
        rows.append(row_str)

    # Объединяем строки с переносами
    matrix_body = "\n".join(rows)

    # Добавляем скобки
    max_row_length = max(len(row) for row in rows)
    top_bracket = left_bracket + " " * (max_row_length + 2) + right_bracket
    bottom_bracket = top_bracket

    return f"{top_bracket}\n {matrix_body}\n{bottom_bracket}"


# Пример использования с греческими символами
if __name__ == "__main__":
    # Матрица с греческими символами (используем Unicode)
    greek_matrix = [
        [1, "λ", 3],
        ["μ", 5, "α"],
        [7, "β", 9]
    ]

    print("Матрица с греческими символами (круглые скобки):")
    display_matrix_with_greek(greek_matrix, "pmatrix")

    print("\nМатрица с греческими символами (квадратные скобки):")
    display_matrix_with_greek(greek_matrix, "bmatrix", font_size=18)

    # Матрица с дробями и греческими символами
    complex_matrix = [
        ["1/2", "λ", "√μ"],
        ["μ", "α²", "βᵢⱼ"],
        ["3.14", "λμ", "0"]
    ]
    print("\nСложная матрица с математическими выражениями:")
    display_matrix_with_greek(complex_matrix, "vmatrix", font_size=14)