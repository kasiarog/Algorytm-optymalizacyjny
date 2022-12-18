import random
import math
import timeit
import copy
import networkx as nx
import matplotlib.pyplot as plt


# generator grafu w postaci macierzy, w której zapisane są wagi krawędzi; jeśli nie ma danej krawędzi, to waga jest 0
# (wartości krawędzi z przedziału 1-30)
def generate_matrix(n):  # n - liczba wierzchołków

    rate = int(0.5 * (n * (n - 1) / 2))  # współczynnik nasycenia 50%
    matrix = []
    for i in range(n):  # tworzenie macierzy n x n wypełnionej nieskończonością i zerami
        matrix.append([])
        for j in range(n):
            matrix[i].append(math.inf)  # wszystko uzupełniamy nieskończonościami
            if i == j:
                matrix[i][j] = 0  # uzupełnienie zerami, gdy krawędź łączy jeden wierzchołek (v,v)

    for _ in range(rate):  # tworzone jest tyle krawędzi ile wynosi współczynnik nasycenia
        v1 = random.randint(0, n - 1)
        v2 = random.randint(0, n - 1)
        while matrix[v1][v2] != math.inf or matrix[v2][v1] != math.inf or v1 == v2:  # jeśli jest już taka krawędź
            v1 = random.randint(0, n - 1)
            v2 = random.randint(0, n - 1)
        value = random.randint(1, 30)
        matrix[v1][v2] = value
        matrix[v2][v1] = value

    return matrix


# tworzenie słownika z grafem na podstawie macierzy, tak aby można było z niego narysować graf
# {'wierzchołek1': (wierzchołek1, wierzchołek2, waga), ...}
def make_dict_from_matrix(matrix):
    dict = {}
    n = len(matrix)
    for i in range(n):  # przejście przez całą macierz
        dict[i] = []  # tworzenie klucza w słowniku dla każdego wierzchołka
        for j in range(n):
            if matrix[i][j] != 0 and matrix[i][j] != math.inf:  # jeśli jest krawędź w macierzy
                dict[i].append((i, j, matrix[i][j]))  # tworzę tupla z v1, v2, wagą

    return dict


# funkcja liczy ilość krawędzi w grafie z danej macierzy
def edges_counter(matrix):
    n = len(matrix)
    edges_count = int(0.5 * (n * (n - 1) / 2))

    return edges_count


# algorytm Dijkstry do znajdowania najkrótszej ścieżki do każdego z wierzchołków
# algorytm zmodyfikowany - nie zwraca ścieżek, tylko same ich wagi
def find_shortest_path_dijkstry(matrix, vert):  # vert podajemy jako wierzchołek, z którego wyznaczamy ścieżki

    n = len(matrix)
    Q = list(range(len(matrix)))  # zbiór Q z nieprzejrzanymi wierzchołkami
    S = []  # zbiór S z przejrzanymi już wierzchołkami
    d = [math.inf for _ in range(n)]  # lista z wagami najkrótszych ścieżek do danego wierzchołka

    d[vert] = 0
    while len(Q) > 0:
        minimal_d = math.inf
        min_index = -1
        for q in Q:  # znajdowanie najmniejszej wartości d dla wierzchołków w Q
            if d[q] < minimal_d:
                minimal_d = d[q]  # minimalne d[q] zapisane do zmiennej, żeby wyciągnąć z niego index wierzchołka
                min_index = q  # index najmniejszej wartości, którą wybieramy
        u = min_index  # przypisanie do u wierzchołka o minimalnym d[q]

        S.append(u)  # przenoszenie u z Q do S
        Q.remove(u)
        neighbours = []  # lista z sąsiadami wierzchołka u
        for i in range(len(matrix[u])):
            if matrix[u][i] != math.inf and matrix[u][i] != 0:
                neighbours.append(i)  # tworzę listę sąsiadów wierzchołka

        for w in neighbours:  # zamysł algorytmu Dijkstry
            if w not in Q:
                continue
            if d[w] > d[u] + matrix[u][w]:
                d[w] = d[u] + matrix[u][w]

    return d  # zwraca tablicę z wartościami najkrótszych ścieżek dla każdego wierzchołka (który jest indeksem tablicy)


# funkcja wyznaczająca najkrótsze ścieżki z każdego wierzchołka do każdego
def find_shortest_paths(matrix):
    n = len(matrix)
    list_of_paths = []  # zwracamy listę list z wagami ścieżek
    for v in range(n):
        list_of_paths.append(find_shortest_path_dijkstry(matrix, v))

    return list_of_paths


# funkcja sprawdza, czy graf jest spójny poprzez przeszukiwanie grafu wgłąb
def DFS_check(matrix):

    def DFS(graph, start, visited):  # przeszukiwanie DFS
        visited[start] = True  # ustawiamy wartość 'start' jako odwiedzony
        for i in range(n):
            if graph[start][i] != math.inf and graph[start][i] != 0 and not visited[i]:
                DFS(graph, i, visited)  # jeśli znajdziemy krawędź i wierzchołek nie był jeszcze odwiedzony, rekurencja
        return visited

    check = True  # jeśli graf można przejść DFS to zmienna ma wartość True
    n = len(matrix)
    visited = [False] * n  # uzupełnianie listy odwiedzonych na False
    DFS(matrix, 0, visited)  # przeszukujemy od wierzchołka 0 i żadna krawędź nie była jeszcze odwiedzona
    for v in visited:
        if not v:  # jeśli w visited jest jakaś wartość False, to graf jest niespójny
            check = False
            break

    return check  # zwraca True, jeśli graf jest spójny


# funkcja sprawdzająca, czy nowa najkrótsza ścieżka ma wagę większą niż 150% poprzedniej wagi
# waga = czas dotarcia z punktu A do B
def check_the_limit(paths, new_paths):  # paths - lista wag starych ścieżek, new_paths - lista wag nowych ścieżek
    n = len(paths)
    condition = True

    for i in range(n):
        for j in range(n):
            if new_paths[i][j] > 1.5*paths[i][j]:  # sprawdzany warunek czy nowa wartość jest większa o 50%
                condition = False
                break
        if not condition:
            break

    return condition  # zwraca True, jeśli warunek jest spełniony


# rysowanie grafów zapisanych w tablicy, na podstawie słownika z krawędziami
# wykorzystanie biblioteki Networkx
def draw_graphs(matrices):
    dicts = []
    G = []
    list_of_edges = []

    for i in range(len(matrices)):
        dicts.append(make_dict_from_matrix(matrices[i]))
        G.append(nx.Graph())  # tworzenie grafu
        G[i].add_nodes_from(dicts[i])  # dodaję wierzchołki
        list_of_edges.append([])

        for el in dicts[i].values():  # tworzenie listy z tuplami reprezentującymi krawędzie, aby z niej dodać do grafu krawędzie
            list_of_edges[i] += el
        G[i].add_weighted_edges_from(list_of_edges[i])

    pos = nx.spring_layout(G[0])
    for i in range(len(matrices)):
        plt.figure(i)
        nx.draw(G[i], pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(G[i], "weight")
        nx.draw_networkx_edge_labels(G[i], pos, edge_labels)

    plt.show()


''' BRUTE FORCE '''
# funckja tworzy listę z liczbami binarnymi zapisaymi w listach, co reprezentuje permutacje krawędzi grafu
def generate_binary_permutations(bits):
    list_of_permutations = []

    for i in range(2**bits):
        binary = bin(i)
        list_of_permutations.append([0 for _ in range(bits)])
        for bit in range(len(binary)-1, 1, -1):
            list_of_permutations[i][bit + bits - len(binary)] = int(binary[bit])

    return list_of_permutations


# tworzenie macierzy z danej permutacji
def make_matrix_from_permutation(matrix, permutation, n):
    edge = 0  # inicjuje numer krawędzi, żeby potem wiedzieć którą krawędź wykluczyć z grafu
    counter = 0  # licznik usuniętych krawędzi
    for i in range(n):  # przejście po elementach macierzy, które się nie powtarzają
        for j in range(i, n):
            # usuwanie krawędzi, jeśli nie ma jej w danej permutacji
            if matrix[i][j] != math.inf and matrix[i][j] != 0:
                if not permutation[edge]:
                    matrix[i][j] = math.inf
                    matrix[j][i] = math.inf
                    counter += 1  # zliczamy krawędzie, które usunięto
                edge += 1  # na której krawędzi obecnie jesteśmy

    return counter  # zwraca licznik usuniętych krawędzi


# funkcja usuwająca kolejne krawędzie z grafu BRUTE FORCEM
# sprawdza wszystkie możliwe rozwiązania - wszystkie podgrafy
def delete_edges_brute_force(matrix):
    n = len(matrix)  # liczba wierzchołków
    edges_count = edges_counter(matrix)  # liczba krawędzi
    paths = find_shortest_paths(matrix)  # ścieżki dla pierwotnego grafu
    solutions = []  # lista z rozwiązaniami - ile krawędzi można usunąć w danym rozwiązaniu
    new_matrices = []  # tablica potrzebna, by odczytać optymalne rozwiązanie - przechowuje macierze rozwiązań

    edges_permutations = generate_binary_permutations(edges_count)  # lista permutacji podgrafów

    for permutation in edges_permutations:  # sprawdzamy każdą permutację
        new_matrix = copy.deepcopy(matrix)  # tworzymy macierz nowo powstającego grafu jako kopię starego
        counter = make_matrix_from_permutation(new_matrix, permutation, n)  # ilość usuniętych krawędzi

        if DFS_check(new_matrix):  # sprawdzenie, czy graf jest spójny
            new_paths = find_shortest_paths(new_matrix)
            if check_the_limit(paths, new_paths):  # jeśli warunek jest spełniony dla danej permutacji
                solutions.append(counter)  # dodajemy do listy rozwiązań bieżące rozwiązanie
                new_matrices.append(new_matrix)

    solution = max(solutions)
    return [solution, new_matrices[solutions.index(solution)]]  # zwraca optymalne rozwiązanie i graf


''' ZACHŁANNY '''
# algorytm zachłanny usuwający najpierw krawędzie o największej wadze
def delete_edges_greedy(matrix):
    n = len(matrix)
    edges = edges_counter(matrix)  # ilość krawędzi
    paths = find_shortest_paths(matrix)  # ścieżki dla pierwotnego grafu
    solutions = []
    new_matrices = []  # tablica potrzebna, by odczytać optymalne rozwiązanie - przechowuje macierze rozwiązań

    for v in range(n):  # przechodzimy algorytmem zachłannym przez wszystkie wierzchołki, żeby rozwiązanie było lepsze
        new_matrix = copy.deepcopy(matrix)  # nowa macierz, którą bedziemy modyfikować
        current_edge = 0  # licznik usuwanych krawędzi
        while current_edge <= edges:  # pętla, w której maksymalnie można dojśc do ostatniej krawędzi
            max_value = 0  # zmienna pomocnicza, do znalezienia maksymalnej wartości
            ind = 0  # indeks maksymalnej wartości
            for vert in range(n):  # znajdowanie największego sąsiada wierzchołka v
                if new_matrix[v][vert] != 0 and new_matrix[v][vert] != math.inf and new_matrix[v][vert] > max_value:
                    max_value = new_matrix[v][vert]  # przypisanie nowej największej wartości
                    ind = vert  # indeks największej wartości
            new_matrix[v][ind] = math.inf  # usuwamy wybraną największą krawędź
            new_matrix[ind][v] = math.inf
            current_edge += 1
            v = ind  # kolejną iterację w while'u zaczynamy od następnego wierzchołka, z którego krawędź usunęliśmy

            if DFS_check(new_matrix):  # sprawdzenie, czy powstały graf jest spójny
                new_paths = find_shortest_paths(new_matrix)
                if check_the_limit(paths, new_paths):  # jeśli warunek jest spełniony
                    solutions.append(current_edge)  # dodajemy do listy rozwiązań bieżące rozwiązanie
                    new_matrices.append(new_matrix)
                else:
                    break
            else:
                break  # jeśli któryś z warunków jest niespełniony, wychodzimy z pętli, a w solutions zostaje ostatnie rozwiązanie

    solution = max(solutions)  # ilość krawędzi do usunięcia
    return [solution, new_matrices[solutions.index(solution)]]  # zwraca rozwiązanie i graf


''' HEURYSTYKA '''
# funckja potrzebna do implementacji heurystyki
# znajduje permutacje, gdy znane są już zera na niektórych miejscach, przez to algorytm będzie szybszy
def generate_predefined_permutations(perm):  # perm - permutacja z określoną liczbą '0' na odpowiednich miejscach (lista)
    bits = len(perm)  # ilość bitów
    positions, permutations = [], []  # positions - zawiera pozycje, na których stoją zera
    for i in range(bits):  # zapisanie, na których miejscach występują zera
        if perm[i] == 0:
            positions.append(i)  # uzupełnienie listy o miejsca, na których są '0'

    if len(positions) == bits:  # jeśli w perm są same '0' to zwracamy wyjściowe dane
        return perm
    elif len(positions) == 0:  # jeśli w perm są same '1' to robimy wszystkie permutacje
        return generate_binary_permutations(bits)

    new_bits = bits - len(positions)  # ilość bitów, które trzeba spermutować
    small_permutations = generate_binary_permutations(new_bits)  # tworzę permutacje o mniejszej liczbie bitów

    for j in range(len(small_permutations)):  # dla każdej podpermutacji
        permutations.append([1 for _ in range(bits)])
        for pos in positions:
            permutations[j][pos] = 0  # uzupełnianie '0' na indeksach z positions
        m = 0  # index przechodzący przez krótkie permutacje new_perm
        for i in range(bits):
            if permutations[j][i] == 1:
                permutations[j][i] = small_permutations[j][m]
                m += 1

    return permutations


# funkcja porównuje 2 macierze i na tej podstawie tworzy permutację (które krawędzie się różnią między sobą)
def compare_matrices(matrix1, matrix2, limit):  # matrix1 zawsze musi być początkowa macierz
    n = len(matrix1)
    permutation = []
    edges_count, ones_count = 0, 0  # edges_count-zliczanie krawędzi, ones_count - zliczanie istniejących krawędzi (licznik jedynek)
    for i in range(n):
        for j in range(i+1, n):
            if matrix1[i][j] != math.inf and matrix2[i][j] == math.inf:  # jeśli w matrix1 nie ma krawędzi, a jest w matrix2
                permutation.append(0)
                edges_count += 1
            elif matrix1[i][j] != math.inf and matrix2[i][j] != math.inf:
                permutation.append(1)
                edges_count += 1
                ones_count += 1

    if ones_count > limit * edges_count:  # jeśli policzonych jedynek jest więcej niż limit, to zwróć false
        return False
    else:
        return permutation


# heurystyka - połączenie algorytmu zachłannego i brute force'a
# szuka algorytmem zachłannym rozwiązania i zatrzymuje się w momencie, kiedy dalej nie jest spełniony warunek,
# wtedy brute force sprawdza pozostałe możliwości, które posiadają dane rozwiązanie zachłanne (czy można jeszcze usunąć jakieś krawędzie)
# chcemy też ograniczyć czas wyonywania, dlatego brute force nie będzie mógł wykonywać się dla dużej ilości wierzchołków
def delete_edges_heuristics(matrix):
    n = len(matrix)
    edges_count = edges_counter(matrix)
    limit_for_bruteforce = 0.7  # limit krawędzi, z których można zrobić brute force'a, żeby zaoszczędzić czas
    paths = find_shortest_paths(matrix)
    solutions = []
    new_matrices = []  # tablica potrzebna, by odczytać optymalne rozwiązanie - przechowuje macierze rozwiązań

    for v in range(n):  # przechodzimy algorytmem zachłannym przez wszystkie wierzchołki, żeby rozwiązanie było lepsze
        new_matrix = copy.deepcopy(matrix)
        previous_matrix = copy.deepcopy(new_matrix)
        while 1:  # pętla, w której maksymalnie można dojść do ostatniej krawędzi
            previous_matrix = copy.deepcopy(new_matrix)
            max_value, ind = 0, 0  # max_value - znajduje maksymalną wartość, ind - indeks max. wartości
            for vert in range(n):  # znajdowanie największego sąsiada wierzchołka vert
                if new_matrix[v][vert] != 0 and new_matrix[v][vert] != math.inf:
                    if new_matrix[v][vert] > max_value:
                        max_value = new_matrix[v][vert]  # przypisanie nowej największej wartości
                        ind = vert  # indeks drugiego wierzchołka największej krawędzi
            new_matrix[v][ind] = math.inf  # usuwamy wybraną największą krawędź
            new_matrix[ind][v] = math.inf

            if DFS_check(new_matrix):  # sprawdzenie, czy graf jest spójny
                new_paths = find_shortest_paths(new_matrix)
                if check_the_limit(paths, new_paths):  # jeśli warunek jest spełniony dla danej permutacji
                    previous_matrix = copy.deepcopy(new_matrix)  # przechowuję obecne rozwiązanie jako to dobre
                    v = ind  # kolejną iterację w while'u zaczynamy od następnego wierzchołka, do którego krawędź usunęliśmy
                else:
                    break
            else:
                break  # kiedy wychodzimy z pętli, w previus_matrix jest punkt wyjściowy do brute force'a

        permutation = compare_matrices(matrix, previous_matrix, limit_for_bruteforce)  # dobra macierz zamieniona na permutację
        if not permutation:  # jeśli funkcja compare_matrices zwróci False, czyli przekroczony został limit bitów dla brute forcea
            continue
        else:
            edges_permutations = generate_predefined_permutations(permutation)

            for perm in edges_permutations:  # sprawdzamy każdą permutację
                new_matrix = copy.deepcopy(matrix)  # tworzymy macierz nowo powstającego grafu jako kopię starego
                counter = make_matrix_from_permutation(new_matrix, perm, n)  # zmienia macierz i zwraca liczbę usuniętych krawędzi

                if DFS_check(new_matrix):  # sprawdzenie, czy graf jest spójny
                    new_paths = find_shortest_paths(new_matrix)
                    if check_the_limit(paths, new_paths):  # jeśli warunek jest spełniony dla danej permutacji
                        solutions.append(counter)  # dodajemy do listy rozwiązań bieżące rozwiązanie
                        new_matrices.append(new_matrix)

    if len(solutions) == 0:
        return "W tym grafie nie można zastosować tego algorytmu"
    else:
        solution = max(solutions)
        return [solution, new_matrices[solutions.index(solution)]]  # zwraca rozwiązanie i graf



if __name__ == "__main__":
    # tworzenie macierzy z grafem
    matrixx = generate_matrix(9)
    for row in matrixx:
        print(row)


    print()
    start_time = timeit.default_timer()
    [greedy_solution, matrix2] = delete_edges_greedy(matrixx)
    print("Optymalne rozwiązanie zachłannego: ", greedy_solution)
    stop_time = timeit.default_timer()
    print("Czas wykonywania zachłannego: ", stop_time - start_time)

    print()
    start_time = timeit.default_timer()
    [bruteforce_solution, matrix3] = delete_edges_brute_force(matrixx)
    print("Optymalne rozwiązanie brute force'a: ", bruteforce_solution)
    stop_time = timeit.default_timer()
    print("Czas wykonywania brute force'a: ", stop_time - start_time)

    start_time = timeit.default_timer()
    [heuristics_solution, matrix1] = delete_edges_heuristics(matrixx)
    print("Rozwiązanie heurystyki: ", heuristics_solution)
    stop_time = timeit.default_timer()
    print("Czas wykonywania heurystyki: ", stop_time - start_time)

    draw_graphs([matrixx, matrix1, matrix2, matrix3])
