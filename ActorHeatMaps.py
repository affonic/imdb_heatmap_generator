import requests
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap as lsc
import json
import numpy as np
import math

Actors = {
    "Leonardo DiCaprio" : "nm0000138",
    "Brad Pitt" : "nm0000093",
    "Tom Hanks" : "nm0000158",
    "Morgan Freeman" : "nm0000151",
    "Robert De Niro" : "nm0000134",
    "Johnny Depp" : "nm0000136",
    "Christian Bale" : "nm0000288",
    "Matt Damon" : "nm0000354",
    "Denzel Washington" : "nm0000243"    
}

def fetch_imdb_data(actor):
    url = f"https://api.imdbapi.dev/names/{Actors.get(actor)}/filmography"

    params = {"pageSize": 50, "categories" : "actor"}
    
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

    with open(f"actor_data/{actor}.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, indent=2, ensure_ascii=False)

    print(all_movies)

def generate_ratings_array(actor):
    try:
        with open(f"actor_data/{actor}.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        fetch_imdb_data(actor)
        with open(f"actor_data/{actor}.json", "r") as file:
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
            f"“{actors[count]}”",         # the caption text
            ha="center", va="top",         # center align horizontally
            fontsize=10, fontstyle="italic", color="white",
            transform=ax.transAxes         # make coords relative to axes
        )
    except IndexError:
        pass


def generate_heat_map(actors): #shows is a list of show titles (as strings)

    rows = math.floor(math.sqrt(len(actors)))
    columns = math.ceil(len(actors) / rows)

    traffic_lights = lsc.from_list("traffic_lights", ["#2b0000", "red", "#FFD300", "green"])

    fig, axes = plt.subplots(rows, columns)
    fig.set_facecolor("black")
    fig.suptitle("IMDB Actor HeatMaps...", color="white", fontsize=50, fontfamily="serif", fontweight="bold", fontstyle="italic")


    axes_flat = axes.flat if rows * columns > 1 else [axes]

    i = 0
    for ax in axes_flat:
        if i >= len(actors):
            subplot_gen(ax, [[]], traffic_lights, i)
            continue
        subplot_gen(ax, generate_ratings_array(actors[i]), traffic_lights, i)
        i+=1
    
    plt.show()

actors = ["Leonardo DiCaprio"]

generate_heat_map(actors)