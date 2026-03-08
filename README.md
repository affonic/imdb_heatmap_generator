## IMDb API Fetcher

This project fetches **all episodes, directors, and TV shows** from the [IMDb API](https://api.imdbapi.dev) and saves the results locally in JSON format.  

### Features
- Handles **pagination** automatically using the `nextPageToken` provided by the API.  
- Supports fetching:
  - 🎬 Episodes (with season, episode number, runtime, ratings, etc.)  
  - 🎥 Directors  
  - 📺 TV Shows  
- Saves results to easy-to-read JSON files with proper indentation.  

### Example Usage
```python
from imdb_fetcher import fetch_all_episodes

# Replace with a valid IMDb show ID
episodes = fetch_all_episodes("tt2861424")  
print(f"Fetched {len(episodes)} episodes")

### Note
All the code is by me, im a very clever boy yes i am. This README tho? completely AI generated, except for this part obviously. I like coding i dont like writing markdown files :,(
