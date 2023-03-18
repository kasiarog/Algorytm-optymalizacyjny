# Algorytm wykluczający optymalną ilość dróg komunikacyjych
********Projekt z przedmiotu Optymalizacja Kombinatoryczna********


******1. Cel projektu******

Celem projektu było stworzenie narzędzia do badania liczby tras komunikacyjnych
w mieście, które można by wykluczyć jednocześnie z użytku. Rozwiązanie problemu
ma być optymalne, tj. wynik ma reprezentować jak największą liczbę wykluczonych
jednocześnie tras.

******2. Streszczenie problemu******

Bardzo często władze miasta wykorzystują dostępne w bieżącej chwili zasoby na
wyremontowanie linii komunikacyjnych w mieście. Tymi liniami mogą być ulice, trakcje tramwajowe, ścieżki rowerowe, chodniki itd. Nieraz jednak przedsięwzięcia te nie są zbytnio przemyślane. Wykluczając dane trasy uniemożliwiane jest mieszkańcom bezproblemowe i szybkie przemieszczanie się po mieście. W projekcie postaram się rozwiązać ten problem.
Program konkretnie mówi o tym, ile tras komunikacyjnych można jednocześnie remontować, tak aby nie komplikować mieszkańcom nadmiernie dojazdów. Innymi słowy - ile linii komunikacyjnych można wykluczyć w tym samym czasie, tak aby czas przejazdu z każdego węzła komunikacyjnego do innego węzła nie przekraczał pewnego limitu. W projekcie tym limitem jest 150% poprzedniego czasu potrzebnego na dojazd z pewnego węzła do innego. Oznacza to, że jeśli najkrótsza trasa z puntku A do punktu B przed remontem zabierała x czasu, tak po odcięciu dróg ma ona zabierać nie więcej niż 1,5x czasu.

******3. Opis rozwiązania******

Rozwiązanie postawionego problemu opiera się głównie na teorii grafów. Grafy
będą zasadniczym narzędziem, którym należy się tutaj posłużyć. Implementacja opiera się na pracy na grafach ważonych. Graf ważony jest reprezentacją mapy miasta, na
którą składają się węzły komunikacyjne, połączone są liniami komunikacyjnymi. Trasy komunikacyjne (krawędzie grafu) posiadają wagi, które reprezentują czasy potrzebne na dotarcie z danego węzła do innego (z wierzchołka A do wierzchołka B grafu). Węzłem komunikacyjnym jest wierzchołek grafu. Po przerobieniu wersji fabularnej problemu na bardziej matematyczną, celem projektu jest znalezienie największej liczby krawędzi, które można usunąć z grafu, pod określonymi warunkami. Tymi warunkami są:
- najkrótsze ścieżki pomiędzy każdą parą wierzchołków w powstałym grafie, nie mogą być dłuższe niż 1, 5 długości odpowiadających im ścieżek w grafie wyjściowym
- nowo powstały graf musi być spójny.

Do sprawdzenia spójności grafu wykorzystano algorytm przeszukiwania grafu w głąb (DFS). Zastosowano odpowiednią funkcję, która wykorzystując ten algorytm może bezpośrednio odpowiedzieć na pytanie, czy graf jest spójny. Do wyznaczenia najkrótszych ścieżek przydatny był algorytm Dijkstry. W głównej części programu, która wprost badała liczbę możliwych do usunięcia krawędzi, zaimplementowane są 3 algorytmy:
1. Brute force
2. Algorytm zachłanny
3. Heurystyka

Każdy z tych algorytmów daje rozwiązanie dopuszczalne, takie które jest zadowalające, jednak nie każde zawsze daje rozwiązanie optymalne.
