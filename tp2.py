import networkx as nx
import matplotlib.pyplot as plt

# Lê um arquivo de entrada contendo as atividades, predecessores e durações
def read_input(filename):
    G = nx.DiGraph()
    with open(filename, "r") as file:
        for line in file:
            parts = line.split()
            start, end, duration = parts[0], parts[1], int(parts[2])
            G.add_edge(start, end, duration=duration)
    return G

# Calcula o tempo mais cedo (TE) para cada nó no gráfico
def calculate_early_times(G):
    early_times = {}
    for node in nx.topological_sort(G):
        if len(G.pred[node]) == 0:
            early_times[node] = 0
        else:
            early_times[node] = max(early_times[predecessor] + G[predecessor][node]['duration'] for predecessor in G.pred[node])
    return early_times

# Calcula o tempo mais tarde (TL) para cada nó no gráfico
def calculate_late_times(G, early_times):
    late_times = {}
    end_node = list(filter(lambda node: len(G.succ[node]) == 0, G.nodes()))[0]
    for node in nx.topological_sort(G):
        late_times[node] = early_times[end_node] - early_times[node]
    return late_times

# Encontra o caminho crítico
def find_critical_path(G, early_times, late_times):
    critical_path = []
    for start, end in G.edges():
        if early_times[start] + G[start][end]['duration'] == early_times[end]:
            critical_path.append((start, end))
    return critical_path

# Função principal
def main(input_file):
    G = read_input(input_file)

    # Calcula o tempo mais cedo
    early_times = calculate_early_times(G)

    # Calcula o tempo mais tarde
    late_times = calculate_late_times(G, early_times)

    # Encontra o caminho crítico
    critical_path = find_critical_path(G, early_times, late_times)

    # Desenha o gráfico PERT
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(start, end): G[start][end]['duration'] for start, end in G.edges()})
    plt.title("Gráfico PERT do Projeto")

    print("Tempo mais cedo (TE):", early_times)
    print("Tempo mais tarde (TL):", late_times)
    print("Caminho Crítico:", critical_path)

    plt.show()

if __name__ == "__main__":
    input_file = "entrada.txt"
    main(input_file)
