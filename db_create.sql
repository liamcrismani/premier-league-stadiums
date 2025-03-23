
-- required install
INSTALL SPATIAL;

-- installing will not load the extension by default
LOAD SPATIAL;
 
CREATE TABLE IF NOT EXISTS clubs (
	club_id INTEGER NOT NULL UNIQUE,
	name VARCHAR NOT NULL,
	established VARCHAR,
	PRIMARY KEY(club_id)
);

CREATE TABLE IF NOT EXISTS stadiums (
	stadium_id INTEGER NOT NULL UNIQUE,
	name VARCHAR NOT NULL,
	capacity INTEGER,
	club_id INTEGER,
	opened VARCHAR,
	closed VARCHAR,
	longitude NUMERIC,
	latitude NUMERIC,
	geom GEOMETRY,
	PRIMARY KEY(stadium_id),
	FOREIGN KEY (club_id) REFERENCES clubs(club_id)
	ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS tickets (
	id INTEGER NOT NULL UNIQUE,
	club_id INTEGER NOT NULL,
	cheapest VARCHAR NOT NULL,
	steapest  VARCHAR NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (club_id) REFERENCES clubs(club_id)
	ON UPDATE CASCADE ON DELETE NO ACTION
);
