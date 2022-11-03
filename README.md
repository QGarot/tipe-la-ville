# TIPE 2022-2023 - La ville

## Description du projet
-	**Elaboration du problème** : un évènement est organisé dans une ville et on souhaite limiter les embouteillages qu’il engendrera. Quelques exemples : marché de Noël de Strasbourg, concert, évènement sportif (Stade de France) etc…
-	**Modélisation de la situation** : utilisation des graphes pour représenter les routes qui mènent à l’évènement. Introduction des réseaux de flot.
-	**Proposition d’une solution** : Dans le réseau de flot, chaque route a une capacité qui est un réel positif. Dans notre cas, la capacité peut représenter le débit maximal de voitures tel qu’il n’y ait pas d’embouteillage sur la voie concernée (cela revient à considérer qu’au-delà de ce débit maximal, des embouteillages peuvent se former). Le flot maximum du réseau routier représente alors le débit maximum de voitures arrivant vers le puits.
On peut alors définir une nouvelle capacité maximum associée à l’évènement qui correspondrait au flot maximum du réseau routier sur une durée de n heures.
-	**Objectifs** :
    - Déterminer la capacité d’une route.
    - Déterminer par l’algorithme de Ford-Fulkerson le débit maximal de voitures.
    - En déduire la capacité maximum de l’évènement qui correspondra au nombre maximum de personnes que peut accueillir l’évènement sans qu’il n’y ait d’embouteillages.
    - Exemple concret
    
## Réseau de flot

### Définition

Un réseau de flot est un graphe orienté $G = (S, A)$ où chaque arête $(u, v) \in A$ possède une *capacité* notée $c((u, v)) \ge 0$.
On distingue deux sommets particuliers : une source $s$ qui est un sommet de degré entrant nul et un puits $t$ qui est un sommet de degré sortant nul.

Un flot dans ce réseau est une fonction $f: S^2 \to R$ qui vérifie :
- $\forall (u, v) \in S^2 : f((u, v)) \le  c((u, v))$.
- $\forall u \in S\setminus \set{s, t} : \sum_{v \in S} f((v, u)) = \sum_{v \in S} f((u, v))$

### Valeur d'un flot f

La *valeur* d'un flot f est défini par $|f| = \sum_{v \in S} [f((s, v)) - f((v, s))]$

Remarque : la source étant de degré entrant nul, le terme $f((v, s))$ de la somme précédente sera en général nulle, mais cette définition plus générale
sera utile dans le cas des réseaux résiduels qu’on verra plus loin.
