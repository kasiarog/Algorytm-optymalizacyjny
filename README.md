# Projekt-OK
Projekt z przedmiotu Optymalizacja Kombinatoryczna (Informatyka, semestr III)


Streszczenie problemu

Celem projektu jest zbadanie jak największej ilości możliwych do wykluczenia tras komunikacyjnych w mieście.

Bardzo często władze miasta wykorzystują dostępne w bieżącej chwili zasoby na wyremontowanie linii komunikacyjnych w mieście. Tymi liniami mogą być ulice, trakcje tramwajowe, ścieżki rowerowe, chodniki itd. Nieraz jednak przedsięwzięcia te nie są zbytnio przemyślane. Wykluczając dane trasy uniemożliwiane jest mieszkańcom bezproblemowe i szybkie przemieszczanie się po mieście. W projekcie postaram się rozwiązać ten problem.

Program konkretnie mówi o tym, ile tras komunikacyjnych można jednocześnie remontować, tak aby nie komplikować mieszkańcom nadmiernie dojazdów. Innymi słowy - ile linii komunikacyjnych można wykluczyć w tym samym czasie, tak aby czas przejazdu z każdego węzła komunikacyjnego do innego węzła nie przekraczał pewnego limitu. W projekcie tym limitem jest 150% poprzedniego czasu potrzebnego na dojazd z pewnego węzła do innego. Oznacza to, że jeśli najkrótsza trasa z puntku A do punktu B przed remontem zabierała x czasu, tak po odcięciu dróg ma ona zabierać nie więcej niż 1,5x czasu.

