import sys
import random

def move_direcao(acao):
    if acao == 'cima':
        return (-1, 0)
    elif acao == 'direita':
        return (0, 1)
    elif acao == 'baixo':
        return (1, 0)
    elif acao == 'esquerda':
        return (0, -1)

def verifica_borda_parede(x, y, mapa, R):
    if x >= len(mapa) or y >= len(mapa[0]) or x < 0 or y < 0:
        return False
    if R[x][y] <= -1000000000:
        return False
    return True

def acao_aleatoria():
    numero_aleatorio = random.uniform(0, 1)
    if numero_aleatorio < 0.25:
        return 'cima'
    elif 0.25 <= numero_aleatorio < 0.5:
        return 'direita'
    elif 0.5 <= numero_aleatorio < 0.75:
        return 'baixo'
    else:
        return 'esquerda'

def movimento_perpendicular(acao, i):
    if acao == 'cima':
        perpendicular = ['esquerda', 'direita']
    elif acao == 'direita':
        perpendicular = ['cima', 'baixo']
    elif acao == 'baixo':
        perpendicular = ['direita', 'esquerda']
    else:
        perpendicular = ['baixo', 'cima']
    return perpendicular[i]


def verifica_acao_valida(acao, x, y, mapa, R):
    x_movimentacao, y_movimentacao = move_direcao(acao)
    if verifica_borda_parede(x + x_movimentacao, y + y_movimentacao, mapa, R):
        return (x_movimentacao, y_movimentacao)
    return (0, 0)


def calcula_q_valor(q_possiveis, q_acao, recompensa):
    alfa = 0.1
    gama = 0.9
    q_maximo = max(q_possiveis.values())
    return q_acao + alfa*(recompensa + gama*q_maximo - q_acao)


def acao_estocastica(acao):
    numero_aleatorio = random.uniform(0, 1)
    if numero_aleatorio < 0.1:
        acao = movimento_perpendicular(acao, 0)
    elif 0.1 <= numero_aleatorio < 0.2:
        acao = movimento_perpendicular(acao, 1)
    return acao


def mover(mapa, Q, R, x, y, estocastico):
    epislon = 0.1
    numero_aleatorio = random.uniform(0, 1)
    if numero_aleatorio < epislon:
        acao = acao_aleatoria()
        x_move, y_move = verifica_acao_valida(acao, x, y, mapa, R)
        return (x+x_move, y+y_move, acao)
    else:
        acao = ''
        maior_q = -10000000
        x_auxiliar, y_auxiliar = 0, 0
        for direcao in ['cima', 'baixo', 'esquerda', 'direita']:
            x_move, y_move = verifica_acao_valida(direcao, x, y, mapa, R)
            valor_q_esperado = calcula_q_valor(Q[x+x_move][y+y_move], Q[x][y][direcao], R[x+x_move][y+y_move])
            if valor_q_esperado > maior_q or R[x+x_move][y+y_move] == 10:
                maior_q = valor_q_esperado
                acao = direcao
                x_auxiliar, y_auxiliar = x_move, y_move
        if estocastico:
            acao = acao_estocastica(acao)
            x_move, y_move = verifica_acao_valida(acao, x, y, mapa, R)
            return (x + x_move, y + y_move, acao)
        return (x+x_auxiliar, y+y_auxiliar, acao)



def Q_learning(mapa, Q, R, x_inicial, y_inicial, passos, estocastico):
    x_auxiliar, y_auxiliar = x_inicial, y_inicial
    for i in range(passos):
        x_destino, y_destino, acao = mover(mapa, Q, R, x_auxiliar, y_auxiliar, estocastico)
        Q[x_auxiliar][y_auxiliar][acao] = calcula_q_valor(Q[x_destino][y_destino],
                                                          Q[x_auxiliar][y_auxiliar][acao],
                                                          R[x_destino][y_destino])
        if R[x_destino][y_destino] in [-10, 0, 10]:
            x_auxiliar, y_auxiliar = x_inicial, y_inicial
        else:
            x_auxiliar, y_auxiliar = x_destino, y_destino
    return True


def monta_mapa_Q_R_negativo(mapa_arq):
    tamanhos = mapa_arq.readline().split(' ')
    mapa = []
    R = []
    Q = []
    for i in range(int(tamanhos[1])):
        mapa.append([])
        R.append([])
        Q.append([])
    for x, linha in enumerate(mapa_arq):
        for y, terreno in enumerate(linha.strip()):
            valor_inicial_Q = 0
            if terreno == '.':
                R[x].append(-0.1)
            elif terreno == ';':
                R[x].append(-0.3)
            elif terreno == '+':
                R[x].append(-1)
            elif terreno == 'x':
                valor_inicial_Q = -10
                R[x].append(-10)
            elif terreno == 'O':
                valor_inicial_Q = 10
                R[x].append(10)
            elif terreno == '@':
                R[x].append(-1000000000)
            mapa[x].append(terreno)
            Q[x].append({
                "cima": valor_inicial_Q,
                "direita": valor_inicial_Q,
                "baixo": valor_inicial_Q,
                "esquerda": valor_inicial_Q
            })
    return (mapa, Q, R)


def monta_mapa_Q_R_positivo(mapa_arq):
    tamanhos = mapa_arq.readline().split(' ')
    mapa = []
    R = []
    Q = []
    for i in range(int(tamanhos[1])):
        mapa.append([])
        R.append([])
        Q.append([])
    for x, linha in enumerate(mapa_arq):
        for y, terreno in enumerate(linha.strip()):
            valor_inicial_Q = 0
            if terreno == '.':
                R[x].append(3)
            elif terreno == ';':
                R[x].append(1.5)
            elif terreno == '+':
                R[x].append(1)
            elif terreno == 'x':
                valor_inicial_Q = 0
                R[x].append(0)
            elif terreno == 'O':
                valor_inicial_Q = 10
                R[x].append(10)
            elif terreno == '@':
                R[x].append(-1000000000)
            mapa[x].append(terreno)
            Q[x].append({
                "cima": valor_inicial_Q,
                "direita": valor_inicial_Q,
                "baixo": valor_inicial_Q,
                "esquerda": valor_inicial_Q
            })
    return (mapa, Q, R)

def pega_melhor_direcao(q_possiveis):
    aux_maior = -1000000000
    direcao_final = ''
    for direcao in q_possiveis.keys():
        if q_possiveis[direcao] > aux_maior:
            direcao_final = direcao
            aux_maior = q_possiveis[direcao]
    return direcao_final

def desenha_direcao(direcao):
    if direcao == 'cima':
        return '^'
    elif direcao == 'direita':
        return '>'
    elif direcao == 'baixo':
        return 'v'
    elif direcao == 'esquerda':
        return '<'

def formata_saida(mapa, Q):
    mapa_desenhado = ''
    for i, linha in enumerate(mapa):
        for j, coluna in enumerate(linha):
            if mapa[i][j] in ['x', 'O', '@']:
                mapa_desenhado += mapa[i][j]
            else:
                mapa_desenhado += desenha_direcao(pega_melhor_direcao(Q[i][j]))
        mapa_desenhado += '\n'
    print(mapa_desenhado)

if __name__ == "__main__":
    nome_mapa = sys.argv[1]
    metodo_utilizado = sys.argv[2]

    x_inicial, y_inicial = int(sys.argv[4]), int(sys.argv[3])

    passos = int(sys.argv[5])

    mapa_arq = open(nome_mapa, "r")

    estocastico = False
    if metodo_utilizado == 'standard':
        mapa, Q, R = monta_mapa_Q_R_negativo(mapa_arq)
    elif metodo_utilizado == 'positive':
        mapa, Q, R = monta_mapa_Q_R_negativo(mapa_arq)
    else: #metodo_utilizado == 'stochastic':
        mapa, Q, R = monta_mapa_Q_R_negativo(mapa_arq)
        estocastico = True

    mapa_arq.close()

    Q_learning(mapa, Q, R, x_inicial, y_inicial, passos, estocastico)

    formata_saida(mapa, Q)
