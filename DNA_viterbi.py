"""ALGORITMO VITERBI

Este modelo se compone de 2 estados, H (alto contenido de GC) y
L (Bajo contenido de GC). Se puede considerar que el estado H caracteriza ADN
codificado mientras que L caracteriza ADN no codificado.

El modelo puede ser usado para predecir la región de ADN codificado para
una secuencia dada.
"""

# SECUENCIA 1
secuencia_1 = ('G', 'G', 'C', 'A', 'C', 'T', 'G', 'A', 'A')

#  SECUENCIA 2
secuencia_2 = ('G', 'G', 'C', 'A')

# ------------ PARAMETROS MODELO MARKOV --------------------------

# Alto, Bajo
estados = ("H", "L")
# Probabilidades iniciales
prob_ini = {"H": 0.5, "L": 0.5}
# Probabilidades de transición
prob_trans = {
    "H": {
        "H": 0.5,
        "L": 0.5
    },  # Reincidencia, transición
    "L": {
        "H": 0.4,
        "L": 0.6
    },
}
# Probabilidad de emisión
prob_emi = {
    "H": {
        "A": 0.2,
        "C": 0.3,
        "G": 0.3,
        "T": 0.2
    },
    "L": {
        "A": 0.3,
        "C": 0.2,
        "G": 0.2,
        "T": 0.3
    },
}

# ----------------------- INICIO DE ALGORITMO -------------------------------


def dptable(V):
    """Tabla de resultados

    Imprime la tabla de pasos a partir de un diccionario Viterbi
    Este diccionario es generado por la función de algoritmo Viterbi.

    Parameters
    ----------
    V: dict
        Diccionario generado por la función viterbi

    Returns
    -------
    Iterator:
        String con la información a imprimir.
    """
    yield " " * 5 + "     ".join(("%3d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%lf" % v[state]["prob"])
                                          for v in V)


def viterbi(obs, states, start_p, trans_p, emit_p):
    """Algoritmo Viterbi

    Algoritmo de viterbi

    Parameters
    ----------
    obs: tuple(str)
        Tupla con la secuencia de observación.
    states: tuple(str)
        Tupla con los estados del modelo HMM.
    start_p: dict
        Diccionario que contiene las probabilidades iniciales en el HMM.
        Las llaves de este diccionario deben coincidir con las estipuladas
        en el parámetro states.
    tras_p: dict
        Diccionario con las probabilidades de transición. La estructura de este
        diccionario está dada por "estado: dict".
    emit_p: dict
        Diccionario con las probabilidades de emisión. La estructura
        de este diccionario está dada por "estado: dict".
    """
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Inicio de iteraciones
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t - 1][states[0]]["prob"] * trans_p[states[0]][st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}

    # Impresión de tabla de resultados
    for line in dptable(V):
        print(line)

    opt = []
    max_prob = 0.0
    best_st = None
    # Obteniendo el estado mas probable y su backtrack
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st

    # Seguimiento del backtrack hasta la primera observación
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print("Los pasos de estado son " + " ".join(opt) +
          " con mayor probabilidad de %s" % max_prob)


if __name__ == "__main__":
    """
    FLUJO PRINCIPAL
    """
    # SECUENCIA 1
    print('\n--------------- SECUENCIA 1-------------------------\n')
    viterbi(secuencia_1, estados, prob_ini, prob_trans, prob_emi)
    # SECUENCIA 2
    print('\n--------------- SECUENCIA 2-------------------------\n')
    viterbi(secuencia_2, estados, prob_ini, prob_trans, prob_emi)
