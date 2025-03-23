PRAGMA trusted_schema = 1;

SELECT load_extension('mod_spatialite');

SELECT InitSpatialMetaData();
        
CREATE TABLE IF NOT EXISTS "clubs" (
	"club_id" INTEGER NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"established" TEXT,
	PRIMARY KEY("club_id")
);

CREATE TABLE IF NOT EXISTS "stadiums" (
	"stadium_id" INTEGER NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"capacity" INTEGER,
	"club_id" INTEGER,
	"opened" TEXT,
	"closed" TEXT,
	"longitude" NUMERIC,
	"latitude" NUMERIC,
	PRIMARY KEY("stadium_id"),
	FOREIGN KEY ("club_id") REFERENCES "clubs"("club_id")
	ON UPDATE CASCADE ON DELETE NO ACTION
);

SELECT AddGeometryColumn('stadiums', 'geom', 3857, 'POINT', 'XY');

CREATE TABLE IF NOT EXISTS "tickets" (
	"id" INTEGER NOT NULL UNIQUE,
	"club_id" INTEGER NOT NULL,
	"cheapest" TEXT NOT NULL,
	"steapest"  TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("club_id") REFERENCES "clubs"("club_id")
	ON UPDATE CASCADE ON DELETE NO ACTION
);