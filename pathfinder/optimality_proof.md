# Une preuve de l'optimalité de l'algorithme A*

Pour toute la suite, on fixe $G = (S, A, w)$ un graphe orienté pondéré par un poids positif.

## Définition : heuristique pour la recherche d'un sommet
Soit $t \in S$.

Une heuristique pour la recherche de $t$ est une application $h : S \to \mathbb{R_+} \mid h(t) = 0$.

## Notation : poids du plus court chemin entre deux sommets
Soit $a, b \in S$.

On note $d(a, b)$ le poids du plus court chemin entre $a$ et $b$, c'est-à-dire :
$d(a, b) = min(\set{w(p) \text{ avec } p \text{ un chemin de } a \text{ à } b})$

## Définition : heuristique admissible
Soient $t \in S$ et $h$ une heuristique pour la recherche de $t$.

On dit que $h$ est *admissible* lorsque $\forall s \in S, h(s) \le d(s, t)$.

Autrement dit, $h$ est *admissible* si h ne surestime jamais le coût de la résolution.

## Proposition :
Soient $s, t \in S$ et $h$ une heuristique admissible pour la recherche de $t$.

L'appel de la fonction implémentant l'algorithme A* avec comme paramètres les sommets $s$ et $t$ retourne un plus court chemin de $s$ à $t$, s'il existe.

#### Démonstration
Quelques notations : pour un sommet $s$ donné, on note $g(s)$ (resp. $f(s)$ ) le coût total pour accéder à $s$ (resp. la priorité de $s$).

Soit $\mathcal{C_A*} = s_0 ... s_m$ le chemin retourné par l'algorithme A*, où $s_0 = s$ et $s_m = t$. On note $d$ le poids de ce chemin. Notons qu'au moment de l'extraction de $t$, sa priorité est $f(t) = g(t) + h(t)$. Comme $h$ est une heuristique pour la recherche de $t$, $h(t) = 0$. Il vient donc que $f(t) = g(t) = d$ **( * )**, puisque $g(t)$ correspond au coût de déplacement total pour aller en $t$.

On suppose maintenant par l'absurde qu'il existe un chemin $\mathcal{C} = a_0 ... a_n$, où $a_0 = s$ et $a_n = t$, de poids minimal $d'$. Ainsi : $d' \le d$.

Montrons par récurrence la propriété suivante : $\forall i \in [\mid0,n\mid], a_i$ prendra la priorité $f(a_i) \le d'$.

- Initialisation ($i = 0$) : $a_i = a_0$.

On a : $f(a_0) = g(a_0) + h(a_0)$

Au début de l'algorithme, le coût ```g``` associé au sommet $a_0$ est initialisé à 0, ce qui signifie exactement que $g(a_0) = 0$.

Donc $f(a_0) = + h(a_0)$.

Or, $h$ est une heuristique admissible pour la recherche de $t$, ce qui implique que $h(a_0) \le d(a_0, t) = d(s, t)$. Notons que $d(s, t) = d'$ puisque par définition, $d(s, t)$ est le poids du plus court chemin de $s$ à $t$.

Donc on a l'inégalité $f(a_0) \le d'$. La propriété à démontrer est alors initialisée.

- Hérédité : soit $i \in [\mid0,n\mid] \mid f(a_i)$ prenne la priorité $f(a_i) \le d'$. Montrons que le sommet $a_{i+1}$ prendra la priorité $f(a_{i+1}) = g(a_{i+1}) + h(a_{i+1}) \le d'$.

Après l'extraction du sommet $a_i$, qui se fait donc avant celle de $t$, l'algorithme parcourt ses voisins. Considérons le sommet $a_{i+1}$. Deux cas de figure se présentent d'après l'algorithme :

*(i)* Premier cas : soit le coût $g(a_{i+1})$ n'est pas encore défini, soit $g(a_i) + w(a_i, a_{i+1}) \lt g(a_{i+1})$. L'algorithme met alors à jour la valeur de ```g``` ; $g(a_{i+1}) = g(a_i) + w(a_i, a_{i+1})$. On peut donc calculer la priorité du sommet $a_{i+1}$, et la majorer ; $f(a_{i+1}) = g(a_{i+1}) + h(a_{i+1}) = g(a_i) + w(a_i, a_{i+1}) + h(a_{i+1})$. L'admissibilité de $h$ permet d'écrire que ; $g(a_i) + w(a_i, a_{i+1}) + h(a_{i+1}) \le g(a_i) + w(a_i, a_{i+1}) + d(a_{i+1}, t) = d'$. On a alors que : $f(a_{i+1}) \le d'$.

*(ii)* Deuxième cas : le coût $g(a_{i+1})$ est déjà défini et le coût courant est plus grand que sa valeur. On a ; $f(a_{i+1}) = g(a_{i+1}) + h(a_{i+1}) \le g(a_{i+1}) + d(a_{i+1}, t)$. La majorant vient toujours du fait que l'heuristique $h$ est admissible. Comme $g(a_{i+1}) + d(a_{i+1}, t) = d'$, on a alors que : $f(a_{i+1}) \le d'$

Dans tous les cas, on obtient la majoration $f(a_{i+1}) \le d'$, ce qui montre que la propriété à démontrer est héréditaire.

- Conclusion : la propriété étant initialisée et héréditaire, alors elle est vraie. Elle est en particulier vraie pour le dernier sommet ; $f(a_n) \le d' \lt d$, ce qui contredit l'égalité désignée par **( * )**. L'hypothèse d'un chemin plus court que celui retourné par A* aboutit à une contradiction, ce qui prouve l'optimalité du chemin renvoyé par l'algorithme A*.
