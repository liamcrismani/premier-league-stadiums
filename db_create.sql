CREATE TABLE IF NOT EXISTS "clubs" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"established" TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "stadiums" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"peak_capacity" INTEGER,
	"current_capacity" INTEGER,
	"club_id" INTEGER NOT NULL,
	"opened" TEXT,
	"closed" TEXT,
    -- TODO: convert to geometry (point)
	"geometry" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY ("club_id") REFERENCES "clubs"("id")
	ON UPDATE CASCADE ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "tickets" (
	"id" INTEGER NOT NULL UNIQUE,
	"stadium_id" INTEGER NOT NULL,
	"season" TEXT NOT NULL,
    "avg_price" NUMERIC NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("stadium_id") REFERENCES "stadiums"("id")
	ON UPDATE CASCADE ON DELETE NO ACTION
);
