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

INSERT INTO stations (`id`, `name`, `localisaion_x`, `localisation_y`, `capacity`, `current_people`) VALUES
(1, 'A', 4, 2, 10, 0),
(2, 'B', 5, 0.5, 10, 0),
(3, 'C', -2, -3.4, 10, 0),
(4, 'D', -3.8, -1.3, 10, 0),
(5, 'E', -1.5, 2.4, 10, 0),
(6, 'F', 2.2, -2.7, 10, 0);