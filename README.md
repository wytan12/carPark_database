# CarPark Database Documentation

## Overview
This repository manages a database for storing car park information and availability. The database tracks carpark locations, lot types (car or motorcycle) and real-time availability for both. It also includes background tasks to scrape and update availability data at regular intervals.

---

## Database Structure

### 1. CarParkInfo
The `CarParkInfo` table stores static information about car parks, such as their ID, name, location, and lot type (car or motorcycle). Each car park can have multiple entries if it supports both cars and motorcycles.

- **Primary Key**: `id` (auto-incremented)
- **Unique Constraint**: Each combination of `carpark_id` and `lot_type` must be unique.

| Field         | Type          | Description                                         |
|---------------|---------------|-----------------------------------------------------|
| `id`          | BigAutoField  | Auto-incremented unique identifier                  |
| `carpark_id`  | CharField     | Unique identifier for the car park (will be duplicated for different lot types) |
| `name`        | CharField     | The name of the carpark                             |
| `lot_type`    | CharField     | Lot type: 'C' for cars and 'Y' for motorcycles      |
| `latitude`    | FloatField    | Latitude of the carpark location                    |
| `longitude`   | FloatField    | Longitude of the carpark location                   |
| `total_capacity` | IntegerField | Total parking capacity for respective lot type      |
| `agency`      | CharField     | Agency managing the carpark, includes CapitaLand, HDB, LTA, and URA.    |
| `last_updated` | DateTimeField | Timestamp when the data was retrieved and stored in the database.   |

### 2. CarParkAvailability
The `CarParkAvailability` table stores real-time availability data for carparks. Each record links to a specific entry in the `CarParkInfo` table.

| Field           | Type          | Description                                         |
|-----------------|---------------|-----------------------------------------------------|
| `id`            | BigAutoField  | Auto-incremented unique identifier                  |
| `info_id`       | ForeignKey    | Foreign key linking to `CarParkInfo.id`             |
| `available_lot` | IntegerField  | Number of lots available at point of data retrieval.    |
| `last_updated`  | DateTimeField | Timestamp when the data was retrieved and stored in the database.  |

---

## Background Tasks
The repository includes a background task that runs every 30 minutes to update carpark real time availability from external sources.

### Task Description
- **Task Name**: `run_tasks()`
- **Frequency**: Every 30 minutes
- **Functions**:
  - `scrape_data()`: Scrapes carpark availability data from CapitaLand
  - `pull_data()`: Calls the LTA API to retrieve real time carpark availability data

---

## Data Constraints

1. **Unique CarPark Entries**: Each carpark can have multiple entries in `CarParkInfo`, but they must have unique combinations of `carpark_id` and `lot_type`. The `id` field serves as the primary key to uniquely track these combinations.

2. **Foreign Key Relationships**: The `CarParkAvailability` table has a foreign key (`info_id`) that references the `id` field in `CarParkInfo`. This links availability records to specific carpark.

---
