import time
import sys
import copy

def verifica_borda(x, y, x_total, y_total):
    if x >= x_total or x < 0:
        return False
    if y >= y_total or y < 0:
        return False
    return True


def monta_mapa_real(mapa_arq):
    tamanhos = mapa_arq.readline().split(' ')
    mapa = []
    grafo = {}
    for i in range(int(tamanhos[1])):
        mapa.append([])
    for x, linha in enumerate(mapa_arq):
        for y, terreno in enumerate(linha.strip()):
            vizinhos = []
            if terreno == '.':
                mapa[x].append(1)
            elif terreno == ';':
                mapa[x].append(1.5)
            elif terreno == '+':
                mapa[x].append(2.5)
            elif terreno == 'x':
                mapa[x].append(6)
            elif terreno == '@':
                mapa[x].append(1234567890)

            if verifica_borda(x+1, y, int(tamanhos[1]), int(tamanhos[0])):
                vizinhos.append(f"{x+1}-{y}")

            if verifica_borda(x-1, y, int(tamanhos[1]), int(tamanhos[0])):
                vizinhos.append(f"{x-1}-{y}")

            if verifica_borda(x, y+1, int(tamanhos[1]), int(tamanhos[0])):
                vizinhos.append(f"{x}-{y+1}")

            if verifica_borda(x, y-1, int(tamanhos[1]), int(tamanhos[0])):
                vizinhos.append(f"{x}-{y-1}")

            grafo[f"{x}-{y}"] = vizinhos.copy()
    return mapa, grafo


def monta_mapa_guloso(mapa, x_destino, y_destino):
    mapa_guloso = copy.deepcopy(mapa)
    for x, linha in enumerate(mapa):
        for y, coluna in enumerate(linha):
            mapa_guloso[x][y] = abs(x - x_destino) + abs(y - y_destino)
    return mapa_guloso


def monta_mapa_A_estrela(mapa, x_destino, y_destino):
    mapa_a_estrela = copy.deepcopy(mapa)
    for x, linha in enumerate(mapa):
        for y, coluna in enumerate(linha):
            mapa_a_estrela[x][y] += abs(x - x_destino) + abs(y - y_destino)
    return mapa_a_estrela


def grafo_pesos_acumulados(grafo, mapa):
    grafo_pesos = {}
    for no in grafo.keys():
        x, y = no.split('-')
        grafo_pesos[no] = mapa[int(x)][int(y)]
    return grafo_pesos


def pega_caminho_menor(fronteira, grafo_com_pesos):
    aux_menor = 1234567890
    aux_indice = 0
    for indice, caminho in enumerate(fronteira):
        if grafo_com_pesos[caminho[-1]] < aux_menor:
            aux_menor = grafo_com_pesos[caminho[-1]]
            aux_indice = indice
    return fronteira.pop(aux_indice)


def pega_caminho_guloso_a_estrela(fronteira, mapa):
    aux_menor = 1234567890
    aux_indice = 0
    for indice, caminho in enumerate(fronteira):
        x, y = caminho[-1].split('-')
        if mapa[int(x)][int(y)] < aux_menor:
            aux_menor = mapa[int(x)][int(y)]
            aux_indice = indice
    return fronteira.pop(aux_indice)

def pega_valor_caminho(caminho, mapa):
    soma = 0
    for posicao in caminho[1:]:
        x, y = posicao.split('-')
        soma += mapa[int(x)][int(y)]
    return soma


def bfs(grafo, inicio, destino):
    fronteira = []
    visitados = []
    fronteira.append([inicio])
    while fronteira:
        caminho = fronteira.pop(0)
        no_atual = caminho[-1]
        visitados.append(no_atual)
        if no_atual == destino:
            return caminho
        for adjacent in grafo.get(no_atual, []):
            if adjacent not in visitados:
                novo_caminho = list(caminho)
                novo_caminho.append(adjacent)
                fronteira.append(novo_caminho)


def ucs(grafo, mapa, inicio, destino):
    fronteira = []
    visitados = []
    grafo_com_pesos = grafo_pesos_acumulados(grafo, mapa)
    fronteira.append([inicio])
    while fronteira:
        caminho = pega_caminho_menor(fronteira, grafo_com_pesos)
        no_atual = caminho[-1]
        visitados.append(no_atual)
        if no_atual == destino:
            return caminho
        for adjacent in grafo.get(no_atual, []):
            if adjacent not in visitados:
                grafo_com_pesos[adjacent] = grafo_com_pesos[adjacent] + grafo_com_pesos[no_atual]
                novo_caminho = list(caminho)
                novo_caminho.append(adjacent)
                fronteira.append(novo_caminho)


def ids(grafo, mapa, inicio, destino):
    for profundidade in range(0, 21):
        fronteira = []
        visitados = []
        grafo_com_pesos = grafo_pesos_acumulados(grafo, mapa)
        fronteira.append([inicio])
        while fronteira:
            caminho = pega_caminho_menor(fronteira, grafo_com_pesos)
            no_atual = caminho[-1]
            visitados.append(no_atual)
            if no_atual == destino:
                return caminho
            if len(caminho) <= profundidade:
                for adjacent in grafo.get(no_atual, []):
                    if adjacent not in visitados:
                        grafo_com_pesos[adjacent] = grafo_com_pesos[adjacent] + grafo_com_pesos[no_atual]
                        novo_caminho = list(caminho)
                        novo_caminho.append(adjacent)
                        fronteira.append(novo_caminho)
            else:
                fronteira = []


def greedy(grafo, mapa, inicio, destino):
    fronteira = []
    visitados = []
    fronteira.append([inicio])
    while fronteira:
        caminho = pega_caminho_guloso_a_estrela(fronteira, mapa)
        no_atual = caminho[-1]
        visitados.append(no_atual)
        if no_atual == destino:
            return caminho
        for adjacent in grafo.get(no_atual, []):
            if adjacent not in visitados:
                novo_caminho = list(caminho)
                novo_caminho.append(adjacent)
                fronteira.append(novo_caminho)


def astar(grafo, mapa, inicio, destino):
    fronteira = []
    visitados = []
    fronteira.append([inicio])
    while fronteira:
        caminho = pega_caminho_guloso_a_estrela(fronteira, mapa)
        no_atual = caminho[-1]
        visitados.append(no_atual)
        if no_atual == destino:
            return caminho
        for adjacent in grafo.get(no_atual, []):
            if adjacent not in visitados:
                novo_caminho = list(caminho)
                novo_caminho.append(adjacent)
                fronteira.append(novo_caminho)


def formata_saida(caminho_encontrado, mapa):
    valor_caminho = pega_valor_caminho(caminho_encontrado, mapa)
    saida_formatada = f'{valor_caminho}'
    for caminho in caminho_encontrado:
        x, y = caminho.split('-')
        saida_formatada = saida_formatada + ' (' + x + ', ' + y + ')'
    return saida_formatada


if __name__ == "__main__":
    mapa_str = sys.argv[1]
    algoritmo_str = sys.argv[2]
    x_partida = int(sys.argv[4])
    y_partida = int(sys.argv[3])
    x_destino = int(sys.argv[6])
    y_destino = int(sys.argv[5])

    mapa_arquivo = open(mapa_str, "r")
    mapa, grafo = monta_mapa_real(mapa_arquivo)
    mapa_arquivo.close()

    caminho_encontrado = []
    if algoritmo_str == 'BFS':
        caminho_encontrado = bfs(grafo, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")

    elif algoritmo_str == 'UCS':
        caminho_encontrado = ucs(grafo, mapa, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")

    elif algoritmo_str == 'IDS':
        caminho_encontrado = ids(grafo, mapa, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")

    elif algoritmo_str == 'Greedy':
        caminho_encontrado = greedy(grafo, monta_mapa_guloso(mapa, x_destino, y_destino), f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")

    elif algoritmo_str == 'Astar':
        caminho_encontrado = astar(grafo, mapa, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")
    
    elif algoritmo_str == "documentacao":
        tempo_inicial = time.time()

        bfs_caminho_encontrado = bfs(grafo, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")
        tempo_bfs = time.time() - tempo_inicial
        print(f"tempo de execucao bfs = {tempo_bfs}, caminho = {formata_saida(bfs_caminho_encontrado, mapa)}")

        ucs_caminho_encontrado = ucs(grafo, mapa, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")
        tempo_ucs = time.time() - tempo_inicial - tempo_bfs
        print(f"tempo de execucao ucs = {tempo_ucs}, caminho = {formata_saida(ucs_caminho_encontrado, mapa)}")
        
        ids_caminho_encontrado = ids(grafo, mapa, f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")
        tempo_ids = time.time() - tempo_inicial - tempo_bfs - tempo_ucs
        print(f"tempo de execucao ids = {tempo_ids}, caminho = {formata_saida(ids_caminho_encontrado, mapa)}")
        
        greedy_caminho_encontrado = greedy(grafo, monta_mapa_guloso(mapa, x_destino, y_destino), f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")
        tempo_greedy = time.time() - tempo_inicial - tempo_bfs - tempo_ucs - tempo_ids
        print(f"tempo de execucao greedy = {tempo_greedy}, caminho = {formata_saida(greedy_caminho_encontrado, mapa)}")
        
        caminho_encontrado = astar(grafo, monta_mapa_A_estrela(mapa, x_destino, y_destino), f"{x_partida}-{y_partida}", f"{x_destino}-{y_destino}")
        tempo_astar = time.time() - tempo_inicial - tempo_bfs - tempo_ucs - tempo_ids - tempo_greedy
        print(f"tempo de execucao astar = {tempo_astar}, caminho = {formata_saida(caminho_encontrado, mapa)}")

    print(formata_saida(caminho_encontrado, mapa))