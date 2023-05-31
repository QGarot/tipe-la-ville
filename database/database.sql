--
-- Structure de la table `scheduled_routes`
--

CREATE TABLE scheduled_routes (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  start_id INT NOT NULL,
  destination_id INT NOT NULL,
  arrival INT NOT NULL
);

--
-- Structure de la table `stations`
--

CREATE TABLE stations (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(255),
  localisation_x FLOAT,
  localisation_y FLOAT,
  current_gondola INT NOT NULL DEFAULT 0
);

--
-- Déchargement des données de la table `stations`
--

INSERT INTO stations (id, name, localisation_x, localisation_y, current_gondola) VALUES
(1, 'test', 658, 303, 0),
(2, 'test', 831, 176, 0),
(3, 'test', 848, 390, 0),
(4, 'test', 810, 521, 0),
(5, 'test', 861, 747, 0),
(6, 'test', 686, 645, 0),
(7, 'test', 668, 522, 0),
(8, 'test', 558, 375, 0);