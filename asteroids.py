#!/usr/bin/env python3
# https://github.com/b00kwrm/asteroids
# Download the list of asteroids from NASA for today and print them out.

import requests
import csv
import datetime

dt = datetime.datetime.today()
today = dt.strftime("%Y-%m-%d")


def download_asteroids(start_date, end_date, api_key):
    "Download asteroid data from NASA"
    base_uri = "https://api.nasa.gov/neo/rest/v1/feed?"
    query_string = f"start_date={start_date}&end_date={end_date}&api_key={api_key}"
    full_url = f"{base_uri}{query_string}"
    r = requests.get(full_url)
    asteroid_data = r.json()
    return asteroid_data


def filter_asteroid_data(asteroid_data, todays_date):
    "Filter asteroid data for total count, name, size, speed, miss distance and danger"
    total_asteroid_count = asteroid_data["element_count"]
    asteroids = []
    for asteroid in asteroid_data["near_earth_objects"][todays_date]:
        filtered_data = {
            "Name": asteroid["name"],
            "Minimum Diameter in Meters": asteroid["estimated_diameter"]["meters"][
                "estimated_diameter_min"
            ],
            "Maximum Diameter in Meters": asteroid["estimated_diameter"]["meters"][
                "estimated_diameter_max"
            ],
            "Potentially Hazardous": asteroid["is_potentially_hazardous_asteroid"],
        }
        for close_approach_data in asteroid["close_approach_data"]:
            filtered_data["Speed (MPH)"] = close_approach_data["relative_velocity"][
                "miles_per_hour"
            ]
            filtered_data["Miss Distance in Miles"] = close_approach_data[
                "miss_distance"
            ]["miles"]
        filtered_data["NASA JPL URL"] = asteroid["nasa_jpl_url"]
        asteroids.append(filtered_data)
    return total_asteroid_count, asteroids


def create_csv(data, output_file):
    "Create a csv from a list of dicts"
    field_names = list(data[0].keys())
    with open(output_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    asteroid_data = download_asteroids(today, today, "DEMO_KEY")
    total_asteroid_count, asteroids = filter_asteroid_data(asteroid_data, today)
    print(
        f"There are {total_asteroid_count} asteroids today! For details see asteroids_{today}.csv"
    )
    create_csv(asteroids, f"asteroids_{today}.csv")
