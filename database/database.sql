--
-- Structure de la table `platforms`
--

CREATE TABLE platforms (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  station_id INT,
  current_people INT,
  target_platform_id INT,
  is_open BOOL
);

--
-- Structure de la table `stations`
--

CREATE TABLE stations (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(255),
  localisation_x FLOAT,
  localisation_y FLOAT,
  capacity INT DEFAULT 25,
  current_people INT NOT NULL DEFAULT 0
);

--
-- Déchargement des données de la table `stations`
--

INSERT INTO `stations` (`id`, `name`, `localisation_x`, `localisation_y`, `capacity`, `current_people`) VALUES
(1, 'test', 658, 303, 25, 0),
(2, 'test', 831, 176, 25, 0),
(3, 'test', 848, 390, 25, 0),
(4, 'test', 810, 521, 25, 0),
(5, 'test', 861, 747, 25, 0),
(6, 'test', 686, 645, 25, 0),
(7, 'test', 668, 522, 25, 0),
(8, 'test', 558, 375, 25, 0);