# Premier League Stadiums

Database of Premier league stadiums

## Summary

- [Introduction](#introduction)
- [Database Type](#database-type)
- [Table Structure](#table-structure)
	- [clubs](#clubs)
	- [stadiums](#stadiums)
	- [tickets](#tickets)
- [Relationships](#relationships)
- [Database Diagram](#database-Diagram)

## Introduction
An attempt at creating a geospatial database, just for fun! Only one geometry type so far, however 🤔

### Objectives
- Create a database of premier league football club stadiums
- Store stadium location as Points
- Visualise in Zoho Analytics with tooltips with extra detail (ticket prices, stadium capacity etc)
- Have fun


## Database type
The below database schema documentation was created with the wonderful [drawDB](https://drawdb.vercel.app/editor) app 😍.  


- **Database system:** SQLite with SpatiaLite
## Table structure

### clubs

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null , unique, autoincrement |  | |
| **name** | TEXT | not null  |  | |
| **established** | TEXT | not null  |  | | 


### stadiums

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null , unique, autoincrement |  | |
| **name** | TEXT | not null  |  | |
| **peak_capacity** | INTEGER | not null  |  | |
| **current_capacity** | INTEGER | not null  |  | |
| **club_id** | INTEGER | not null  | fk_stadiums_club_id_clubs | |
| **opened** | TEXT | not null  |  | |
| **closed** | TEXT | not null  |  | |
| **geometry** | TEXT | not null  |  | | 


### tickets

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **id** | INTEGER | 🔑 PK, not null , unique, autoincrement |  | |
| **stadium_id** | INTEGER | not null  | fk_tickets_stadium_id_stadiums | |
| **season** | TEXT | not null  |  | | 


## Relationships

- **stadiums to clubs**: one_to_many
- **tickets to stadiums**: one_to_many

## Database Diagram

```mermaid
erDiagram
	stadiums ||--o{ clubs : references
	tickets ||--o{ stadiums : references

	clubs {
		INTEGER id PK
		TEXT name
		TEXT established
	}

	stadiums {
		INTEGER id PK
		TEXT name
		INTEGER peak_capacity
		INTEGER current_capacity
		INTEGER club_id FK
		TEXT opened
		TEXT closed
		TEXT geometry
	}

	tickets {
		INTEGER id PK
		INTEGER stadium_id FK
		TEXT season
	}
```