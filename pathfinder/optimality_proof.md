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

## Proposition : optimalité de l'algorithme A*, implémenté par la méthode ```pathfinder```
Soient $s, t \in S$ et $h$ une heuristique admissible pour la recherche de $t$.
Si l'appel de la méthode ```pathfinder``` avec comme paramètres les sommets $s$ et $t$ retourne un chemin, alors ce dernier est un plus court chemin de $s$ à $t$.

#### Démonstration
Quelques notations : pour un sommet $s$ donné, on note $g(s)$ (resp. $f(s)$ ) le coût total pour accéder à $s$ (resp. la priorité de $s$).

Soit $\mathcal{C_A*} = s_0 ... s_m$ le chemin retourné par l'algorithme A*, où $s_0 = s$ et $s_m = t$. On note $d$ le poids de ce chemin. Notons qu'au moment de l'extraction de $t$, sa priorité est $f(t) = g(t) + h(t)$. Comme $h$ est une heuristique pour la recherche de $t$, $h(t) = 0$. Il vient donc que $f(t) = g(t) = d$ (désignons par $\star$ cette égalité), puisque $g(t)$ correspond au coût de déplacement total pour aller en $t$.

On suppose maintenant par l'absurde qu'il existe un chemin $\mathcal{C} = a_0 ... a_n$, où $a_0 = s$ et $a_n = t$, de poids minimal $d'$. Ainsi : $d' \lt d$.

Montrons par récurrence la propriété suivante : $\forall i \in [\mid0,n\mid], g(a_i) = d(s, s_i)$ et  $f(a_i) \le d'$.

- Initialisation ($i = 0$) :

D'une part : $g(a_i) = g(a_0)$ et $g(a_0) = 0$ puisqu'au début de l'algorithme, le coût ```g``` associé au sommet $a_0$ est initialisé à 0. De plus, $d(s, a_i) = d(s, a_0) = d(s, s) = 0$, donc $g(a_0) = d(s, a_0)$ car le poids est positif.

D'autre part : $f(a_i) = f(a_0) = g(a_0) + h(a_0) = h(a_0) = h(s)$. Or, $h$ est une heuristique admissible pour la recherche de $t$, ce qui implique que $h(s) \le d(s, t)$. Notons que $d(s, t) = d'$ puisque par définition, $d(s, t)$ est le poids du plus court chemin de $s$ à $t$. On obtient donc l'inégalité $f(a_0) \le d'$.

Le sommet de départ vérifie les deux conditions de la propriété que l'on cherche à démontrer : elle est donc initialisée.

- Hérédité : soit $i \in [\mid0,n\mid] \mid g(a_i) = d(s, a_i)$ et $f(a_i) \le d'$. Montrons que $g(a_{i+1}) = d(s, a_{i+1})$ et $f(a_{i+1}) \le d'$.

Tout d'abord, d'après l'hypothèse de récurrence, le sommet $a_i$ possède la priorité : $f(a_i) \le d' \lt d$. Il est donc extrait avant le sommet $t$. Considérons maintenant son voisin $a_{i+1}$ et distinguons deux cas, imposés par l'algorithme :

1. Si $g(a_{i+1})$ n'est pas défini ou si $g(a_{i+1})$ est défini et que $g(a_i) + w(a_i, a_{i+1}) \lt g(a_{i+1})$ ;

Alors l'algorithme attribue à $g(a_{i+1})$ la valeur $g(a_i) + w(a_i, a_{i+1})$, donc à ce stade, $g(a_{i+1}) = g(a_i) + w(a_i, a_{i+1})$. Or, par hypothèse de récurrence, $g(a_i) = d(s, a_i)$. On déduit donc que $g(a_{i+1}) = d(s, a_i) + w(a_i, a_{i+1}) = d(s, a_{i+1})$. (En effet, si $d(s, a_i) + w(a_i, a_{i+1}) \gt d(s, a_{i+1})$, alors le chemin $s a_1 ... a_i a_{i+1}$ ne serait pas un chemin de poids minimal de $s$ à $a_{i+1}$. Il existerait donc un chemin $s ... a_{i+1}$, noté $\mathcal{L}$, tel que $w(\mathcal{L}) \lt w(s a_1 ... a_i a_{i+1})$. Notons $\mathcal{\widetilde{L}}$ le chemin $\mathcal{L} a_{i+1}a_{i+2}...t$. On aurait donc $w(\mathcal{\widetilde{L}}) = w(\mathcal{L}) + w(a_{i+1}a_{i+2}...t) \lt w(s... a_i a_{i+1}) + w(a_{i+1}a_{i+2}...t) = w(\mathcal{C})$. Or, le chemin $\mathcal{C}$ est un plus court chemin de $s$ à $t$, donc $w(\mathcal{C}) = d(s, t)$ ce qui impliquerait que $w(\mathcal{\widetilde{L}}) \lt d(s, t)$ : c'est absurde).

De plus, $g(a_{i+1})$ étant maintenant défini, on peut calculer $f(a_{i+1})$ : $f(a_{i+1}) = g(a_{i+1}) + h(a_{i+1})$. Or, $h$ est admissible donc $h(a_{i+1}) \le d(a_{i+1}, t)$. On a alors que : $f(a_{i+1}) \le  d(s, a_{i+1}) + d(a_{i+1}, t) = d'$.

2. Sinon, $g(a_{i+1})$ est déjà défini et $g(a_{i+1}) \le g(a_i) + w(a_i, a_{i+1})$ ;

Par hypothèse de récurrence sur $g(a_i)$, on a $g(a_{i+1}) \le d(s, a_i) + w(a_i, a_{i+1})$, donc nécessairement $g(a_{i+1}) = d(s, a_i) + w(a_i, a_{i+1})$ par minimalité de $d(s, a_i)$. On établit alors que $g(a_{i+1}) = d(s, a_{i+1})$.

En reprenant le même raisonnement fait précédemment pour la majoration de $f(a_{i+1})$, on a : $f(a_{i+1}) \le d'$.

Ainsi, dans tous les cas, la propriété est héréditaire.

- Conclusion : la propriété étant initialisée et héréditaire, elle est alors vraie. Elle est en particulier vraie pour le dernier sommet $t$ ; $f(t) = f(a_n) \le d' \lt d$, ce qui contredit l'égalité désignée par $\star$. L'hypothèse d'un chemin plus court que celui retourné par A* aboutit à une contradiction, ce qui prouve l'optimalité du chemin renvoyé par l'algorithme A*.
