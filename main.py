import pandas as pd
import geopandas as gpd
import duckdb

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
stadiums.to_crs("EPSG:3857")

# Create tickets table
# Query web page to get list of HTML tables
tickets_result = pd.read_html(
    "https://www.90min.com/posts/2023-24-premier-league-season-ticket-prices"
    )

# Only one table, at index 0
tickets = tickets_result[0]
tickets.columns = ["club", "cheapest", "steapest"]

# Merge with clubs to get IDs
tickets = tickets.merge(clubs, how="inner", left_on="club", right_on="name")
tickets.drop(columns=["name", "club"], axis=1, inplace=True)

# Create ID column
tickets.insert(0, "id", range(1, 1+len(tickets)))

# Create database
