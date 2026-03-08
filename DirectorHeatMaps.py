import requests
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap as lsc
import json
import numpy as np
import math

Directors = {
    "Quentin Tarantino" : "nm0000233",
    "Christopher Nolan" : "nm0634240",
    "James Cameron" : "nm0000116",
    "Ridley Scott" : "nm0000631",
    "Martin Scorsese" : "nm0000217",
    "Peter Jackson" : "nm0001392",
    "Tim Burton" : "nm0000318",
    "Paul Thomas Anderson" : "nm0000759",
    "Steven Spielberg" : "nm0000229",
    "Wes Anderson" : "nm0027572",
    "Edgar Wright" : "nm0942367"
}

def fetch_imdb_data(director):
    url = f"https://api.imdbapi.dev/names/{Directors.get(director)}/filmography"

    params = {"pageSize": 50, "categories" : "director"}
    
    all_movies = []

    while True:
        response = requests.get(url, params)
        response.raise_for_status()
        data = response.json()

        all_movies.extend(data.get("credits", []))

        next_page = data.get("nextPageToken")
        if not next_page:
            break
        params["pageToken"] = next_page

    with open(f"director_data/{director}.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, indent=2, ensure_ascii=False)

    print(all_movies)

def generate_ratings_array(director):
    try:
        with open(f"director_data/{director}.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        fetch_imdb_data(director)
        with open(f"director_data/{director}.json", "r") as file:
            data = json.load(file)

    all_movies = []

    for title in data:
        if "rating" not in title.get("title") or title.get("title").get("type") == "short": # or "unknown" in episode.get("season") or not episode.get("episodeNumber"):
            continue #havent decided yet if anything needs to be filters. safer to keep this line i guess
        rating = title.get("title").get("rating").get("aggregateRating")
        releaseYear = title.get("title").get("startYear")
        all_movies.append([int(releaseYear), rating])
    
    sorted_movies = sorted(all_movies, key=lambda ep: ep[0])

    print(sorted_movies, all_movies)

    rows = math.floor(math.sqrt(len(sorted_movies)))
    columns = math.ceil(len(sorted_movies) / rows)

    Ratings2D = []
    gridCounter = 0
    currSeason = []
    for episode in sorted_movies:
        if gridCounter == columns:
            gridCounter = 0
            Ratings2D.append(currSeason)
            currSeason = []
        currSeason.append(float(episode[1])/10)
        gridCounter += 1
    Ratings2D.append(currSeason)

    padded = [season + [np.nan]*(columns - len(season)) for season in Ratings2D]
    return np.array(padded)

def subplot_gen(ax, Ratings2D, cmap, count):

    norm = colors.Normalize(vmin=0, vmax=1)

    ax.imshow(Ratings2D, cmap=cmap, norm=norm, interpolation="nearest")
    ax.axis("off")
    try:
        ax.text(
            0.5, -0.1,                     # x, y in axis coordinates (0–1 range)
            f"“{directors[count]}”",         # the caption text
            ha="center", va="top",         # center align horizontally
            fontsize=10, fontstyle="italic", color="white",
            transform=ax.transAxes         # make coords relative to axes
        )
    except IndexError:
        pass


def generate_heat_map(directors): #shows is a list of show titles (as strings)

    rows = math.floor(math.sqrt(len(directors)))
    columns = math.ceil(len(directors) / rows)

    traffic_lights = lsc.from_list("traffic_lights", ["#2b0000", "red", "#FFD300", "green"])

    fig, axes = plt.subplots(rows, columns)
    fig.set_facecolor("black")
    fig.suptitle("IMDB Director HeatMaps...", color="white", fontsize=50, fontfamily="serif", fontweight="bold", fontstyle="italic")


    axes_flat = axes.flat if rows * columns > 1 else [axes]

    i = 0
    for ax in axes_flat:
        if i >= len(directors):
            subplot_gen(ax, [[]], traffic_lights, i)
            continue
        subplot_gen(ax, generate_ratings_array(directors[i]), traffic_lights, i)
        i+=1
    
    plt.show()

directors = ["Quentin Tarantino", "Christopher Nolan",
    "James Cameron", "Ridley Scott", "Martin Scorsese",
    "Peter Jackson", "Tim Burton", "Paul Thomas Anderson",
    "Steven Spielberg", "Wes Anderson", "Edgar Wright"]

generate_heat_map(directors)