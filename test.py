import pandas as pd
import geopandas as gpd
import sqlite3
import sqlalchemy
from sqlalchemy import text

# URL to Wikipedia table
url = "https://en.wikipedia.org/wiki/List_of_Premier_League_stadiums"

# Extract data from HTML with Pandas
df_list: list[pd.DataFrame] = pd.read_html(url)
df: pd.DataFrame = df_list[0]

# Clean data
df.drop(
    ["Image", "Location", "Pitch length (m)", "Pitch width (m)", "Ref."],
    axis=1, inplace=True
)
df["Capacity"] = df["Capacity"].str.strip("†")
df["Capacity"] = df["Capacity"].str.replace(",", "")
df["Opened"] = df["Opened"].str.replace("[18]", "")
df["Closed"] = df["Closed"].astype(str).str.strip(".00")
df.rename(columns={"Stadium": "name"}, inplace=True)

# Relabel columns
df.columns = [col.lower() for col in df.columns]

# Create ID columns
df.insert(1, "club_id", range(1, 1+len(df)))
df.insert(0, "stadium_id", range(1, 1+len(df)))

# Create tables
clubs = df[["club_id", "club"]].drop(59) # Wembley does not have a club
clubs.columns = ["club_id", "name"]
stadiums = df.drop(axis=1, columns=["club"])

# Sort coordinates
stadiums["latitude"] = stadiums["coordinates"].str.extract(r"(\d{2}.\d{5})")
stadiums["longitude"] = stadiums["coordinates"].str.extract(
    r"(\s{1}\d{1}.\d{5})"
    )

# Longitude should be negative for these points
stadiums["longitude"] = stadiums["longitude"].str.replace(" ", "-")

# No longer needed
stadiums.drop("coordinates", axis=1, inplace=True)

# Convert to GeoDataFrame
stadiums = gpd.GeoDataFrame(stadiums)
stadiums = gpd.GeoDataFrame(
    stadiums,
    geometry=gpd.points_from_xy(
        stadiums.longitude, stadiums.latitude, crs="EPSG:4326"
        )
)

# Reproject to Web Mercator
#stadiums.to_crs("EPSG:3857")

# Convert to text for SQL import
stadiums["geom"] = stadiums.geometry.astype(str)
stadiums["geom"] = stadiums["geom"].str.replace(" ", "", n=1)
stadiums["geom"] = "GeomFromText('" + stadiums["geom"].astype(str) + "', 3857)"
stadiums.drop("geometry", axis=1, inplace=True)

# Query web page to get list of HTML tables
tickets_result = pd.read_html(
    "https://www.90min.com/posts/2023-24-premier-league-season-ticket-prices"
    )

# Only one table, at index 0
tickets = tickets_result[0]
tickets.columns = ["club", "cheapest", "dearest"]

# Merge with clubs to get IDs
tickets = tickets.merge(clubs, how="inner", left_on="club", right_on="name")
tickets.drop(columns=["name", "club"], axis=1, inplace=True)

# Create ID column
tickets.insert(0, "id", range(1, 1+len(tickets)))

# Create database
db = sqlite3.connect("stadiums.sqlite")

# Create connection engine
engine = sqlalchemy.create_engine("sqlite:///stadiums.sqlite")

with engine.connect() as conn:

    # Enable Spatialite
    # conn.execute(text("PRAGMA trusted_schema = 1;"))
    # conn.execute(text(
    #     """.load mod_spatialite"""
    # ))

    # conn.execute(text(
    #     """SELECT InitSpatialMetaData();
    #     """
    # ))
    
    # # Create tables
    # conn.execute(text(
    #     """
    #     CREATE TABLE IF NOT EXISTS "clubs" (
    #         "club_id" INTEGER NOT NULL UNIQUE,
    #         "name" TEXT NOT NULL,
    #         "established" TEXT,
    #         PRIMARY KEY("club_id")
    #     );

    #     CREATE TABLE IF NOT EXISTS "stadiums" (
    #         "stadium_id" INTEGER NOT NULL UNIQUE,
    #         "name" TEXT NOT NULL,
    #         "peak_capacity" INTEGER,
    #         "current_capacity" INTEGER,
    #         "club_id" INTEGER,
    #         "opened" TEXT,
    #         "closed" TEXT,
    #         "longitude" NUMERIC,
    #         "latitude" NUMERIC,
    #         PRIMARY KEY("stadium_id"),
    #         FOREIGN KEY ("club_id") REFERENCES "clubs"("club_id")
    #         ON UPDATE CASCADE ON DELETE NO ACTION
    #     );

    #     SELECT AddGeometryColumn('stadiums', 'geom', 3857, 'POINT', 'XY');

    #     CREATE TABLE IF NOT EXISTS "tickets" (
    #         "id" INTEGER NOT NULL UNIQUE,
    #         "club_id" INTEGER NOT NULL,
    #         "cheapest" TEXT NOT NULL,
    #         "steapest"  TEXT NOT NULL,
    #         PRIMARY KEY("id"),
    #         FOREIGN KEY ("club_id") REFERENCES "clubs"("club_id")
    #         ON UPDATE CASCADE ON DELETE NO ACTION
    #     );"""
    # ))

    # Import data
    clubs.to_sql(name="clubs", con=conn, if_exists="replace", index=False)
    stadiums.to_sql(name="stadiums", con=conn, if_exists="replace", index=False)
    tickets.to_sql(name="tickets", con=conn, if_exists="replace", index=False)

    conn.execute("""INSERT INTO stadiums (
                    stadium_id, name, capacity, opened, closed, longitude,
                    latitude, GeomFromText('geom', 3857)
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                        (stadium.stadium_id, stadium.name, stadium.capacity,
                        stadium.opened, stadium.closed, stadium.longitude,
                        stadium.latitude, stadium.geom),

    conn.close()


