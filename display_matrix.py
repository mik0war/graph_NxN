from matplotlib import pyplot as plt

import builder
import visualizer

BUFFER_SIZE = 3

edges = builder.generate_states(BUFFER_SIZE)
states = builder.get_states_array(BUFFER_SIZE)
MATRIX_SIZE = states.__len__()
print(f'Всего состояний: {MATRIX_SIZE}')
kolm = builder.build_equals(states, edges)

plt.rcParams.update({
        "text.usetex": True,
        "text.latex.preamble": r"\usepackage{amsmath}"
    })

matrix_view = builder.build_matrix_view(MATRIX_SIZE, kolm)

latex_matrix = visualizer.matrix_to_latex(matrix_view)

kolm_latex = visualizer.kolm_to_latex(kolm, states)

visualizer.display_latex(latex_matrix, font_size=12)
visualizer.display_latex(kolm_latex, font_size=12)

plt.show()
