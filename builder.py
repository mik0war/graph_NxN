def generate_states(n):
    edges_with_labels = []
    for i in range(n+1):
        for j in range(n+1):
            if i+j > n:
                continue
            if i-1>= 0:
                edges_with_labels.append((f'{i}{j}', f'{i-1}{j}', {'label': r'\mu_2', 'color': 'red'}))
            if j + 1 + i <= n:
                edges_with_labels.append((f'{i}{j}' ,f'{i}{j+1}', {'label': r'\lambda_1', 'color': 'yellow'}))
            if i+j<=n and j-1 >= 0:
                edges_with_labels.append((f'{i}{j}', f'{i+1}{j-1}', {'label': r'\lambda_2', 'color': 'black'}))
            if j == 0 and i+1 <= n:
                edges_with_labels.append((f'{i}{j}', f'{i + 1}{j}', {'label': r'\lambda_2', 'color': 'black'}))
            if j-1>=0:
                edges_with_labels.append((f'{i}{j}', f'{i}{j - 1}', {'label': r'\mu_1', 'color': 'grey'}))

    return edges_with_labels

def get_states_array(n):
    pos = []
    for i in range(n + 1):
        for j in range(n + 1):
            if i + j > n:
                continue

            pos.append(f'{i}{j}')
    return pos

def get_pos_array(n):
    pos = {}
    for i in range(n+1):
        for j in range(n+1):
            if i + j > n:
                continue

            pos[f'{i}{j}'] = (j, n - i)
    return pos

def build_equals(states_array, edges_with_labels):
    kolm = [[] for _ in range(states_array.__len__())]

    for edge in edges_with_labels:
        x = states_array.index(edge[0])
        y = states_array.index(edge[1])
        kolm[x].append({'sign': -1, 'value': edge[2]["label"], 'state': x})
        kolm[y].append({'sign': 1, 'value': edge[2]["label"], 'state': x})
    return kolm


def build_matrix(matrix_size, kolm_system, mu1, mu2, lam1, lam2):
    mm = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

    for index, kol in enumerate(kolm_system):
        for val in kol:
            mm[index][val['state']] += val["sign"] * find_value(val["value"], mu1, mu2, lam1, lam2)

    return mm

def find_value(value, mu1, mu2, lam1, lam2):

    dict_values = {
        r'\lambda_1': lam1,
        r'\lambda_2': lam2,
        r'\mu_1': mu1,
        r'\mu_2': mu2
    }
    return dict_values[value]


def build_matrix_view(matrix_size, kolm_system):
    mm = [['' for _ in range(matrix_size)] for _ in range(matrix_size)]

    for index, kol in enumerate(kolm_system):
        for val in kol:
            mm[index][val['state']] += f'{val["sign"]}'[:-1] + val["value"]

    for index_line, line in enumerate(mm):
        for index_element, element in enumerate(line):
            if not element:
                mm[index_line][index_element] = '0'

    return mm


