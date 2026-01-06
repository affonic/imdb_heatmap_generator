import requests
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap as lsc
import json
import numpy as np
import math

Shows = {
    "Rick and Morty" : "tt2861424",
    "Archer" : "tt1486217",
    "BreakingBad" : "tt0903747",
    "ParksAndRecreation" : "tt1266020",
    "AOT" : "tt2560140",
    "Red vs Blue" : "tt0401747",
    "TeenWolf" : "tt1567432",
    "The Simpsons" : "tt0096697",
    "ModernFamily" : "tt1442437",
    "South Park" : "tt0121955",
    "GameOfThrones" : "tt0944947",
    "House MD" : "tt0412142",
    "HIMYM" : "tt0460649",
    "Friends" : "tt0108778",
    "Brooklyn99" : "tt2467372",
    "TheOffice" : "tt0386676",
    "TheSopranos" : "tt0141842",
    "TheWire" : "tt0306414",
    "Bojack" : "tt3398228",
    "Futurama" : "tt0149460",
    "StrangerThings" : "tt4574334",
    "Lost" : "tt0411008",
    "Dexter" : "tt0773262",
    "Suits" : "tt1632701",
    "LoveDeathRobots" : "tt9561862",
    "BobsBurgers" : "tt1561755",
    "DeathNote" : "tt0877057",
    "DerryGirls" : "tt7120662",
    "PrettyLittleLiars" : "tt1578873",
    "Merlin" : "tt1199099",
    "American Sweethearts: Dallas Cowboys Cheerleaders" : "tt32146518",
    "True Detective" : "tt2356777",
    "Sherlock" : "tt1475582",
    "Avatar" : "tt0417299"
}

def fetch_imdb_data(show_name):
    url = f"https://api.imdbapi.dev/titles/{Shows.get(show_name)}/episodes"

    params = {"pageSize": 50}
    
    all_episodes = []

    while True:
        response = requests.get(url, params)
        response.raise_for_status()
        data = response.json()

        all_episodes.extend(data.get("episodes", []))

        next_page = data.get("nextPageToken")
        if not next_page:
            break
        params["pageToken"] = next_page

    with open(f"show_data/{show_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)

    print(all_episodes)

def generate_ratings_array(show_name):
    try:
        with open(f"show_data/{show_name}.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        fetch_imdb_data(show_name)
        with open(f"show_data/{show_name}.json", "r") as file:
            data = json.load(file)

    all_episodes = []

    for episode in data:
        if "rating" not in episode or "unknown" in episode.get("season") or not episode.get("episodeNumber"):
            continue
        rating = episode.get("rating").get("aggregateRating")
        epNum = episode.get("episodeNumber")
        season = episode.get("season")
        all_episodes.append([int(season), int(epNum), rating])
    
    sorted_episodes = sorted(all_episodes, key=lambda ep: (ep[0], ep[1]))

    Ratings2D = []
    currSeasonNum = "1"
    currSeason = []
    for episode in sorted_episodes:
        if episode[0] is not currSeasonNum:
            currSeasonNum = episode[0]
            Ratings2D.append(currSeason)
            currSeason = []
        currSeason.append(float(episode[2])/10)
    Ratings2D.append(currSeason)

    maxEps = max(len(season) for season in Ratings2D)
    padded = [season + [np.nan]*(maxEps - len(season)) for season in Ratings2D]
    return np.array(padded)

def subplot_gen(ax, Ratings2D, cmap, count):

    norm = colors.Normalize(vmin=0.4, vmax=1)

    ax.imshow(Ratings2D, cmap=cmap, norm=norm, interpolation="nearest")
    ax.axis("off")
    ax.text(
        0.5, -0.1,                     # x, y in axis coordinates (0–1 range)
        f"“{fav_shows[count]}”",         # the caption text
        ha="center", va="top",         # center align horizontally
        fontsize=10, fontstyle="italic",
        transform=ax.transAxes         # make coords relative to axes
    )


def generate_heat_map(shows): #shows is a list of show titles (as strings)

    rows = math.floor(math.sqrt(len(shows)))
    columns = math.ceil(len(shows) / rows)

    traffic_lights = lsc.from_list("traffic_lights", ["#2b0000", "red", "#FFD300", "green"])

    fig, axes = plt.subplots(rows, columns)
    fig.set_facecolor("white")
    fig.suptitle("IMDB HeatMaps...", fontsize=50, fontfamily="Aerial", fontweight="bold")


    axes_flat = axes.flat if rows * columns > 1 else [axes]

    i = 0
    for ax in axes_flat:
        if i >= len(shows):
            subplot_gen(ax, [[]], traffic_lights)
            continue
        subplot_gen(ax, generate_ratings_array(shows[i]), traffic_lights, i)
        i+=1
    
    plt.show()

shows_for_heatmap = ["AOT", "BreakingBad", "Archer", "HIMYM", "Friends", "Bojack", 
                     "RickAndMorty", "ParksAndRecreation", "House", 
                     "RvB", "Simpsons", "ModernFamily", "GameOfThrones",
                     "TheOffice", "Brooklyn99", "SouthPark", "TheSopranos", "TheWire",
                     "Futurama", "StrangerThings", "Lost", "Dexter", "Suits", "TeenWolf",
                     "LoveDeathRobots", "DerryGirls", "DeathNote", "BobsBurgers", "PrettyLittleLiars"]

requested_shows = ["RvB", "Merlin", "American Sweethearts: Dallas Cowboys Cheerleaders",
                   "True Detective", "SouthPark", "Sherlock", "GameOfThrones", "BreakingBad", "Avatar"]
generate_heat_map(requested_shows)    