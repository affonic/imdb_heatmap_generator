📊 IMDB Heatmap Generator 🎥

Generate heatmaps for your favourite TV shows!

✨ Technologies

Python
IMDB API

🚀 Features

Stores the data after it calls the API so it only needs to call once per show.

📍 The Process

I love tv show heat maps and although there are some good tools for generating I thought that all those tools are out of date. I think that what's happened is that those tools collected most of the data with scraping a once and haven't updates. You will call it and it won't show enough seasons for your desired show or the episodes themselves will have slightly inaccurate values. Anyway I figured I could make my own tool that calls the API directly and thus would be perfectly up to date. I wrote this script before I got super into leetcoding so I honestly feel a little nauseus reading the code. Leaves a lot to be desired.

📍 Future Features / How to Help

Inputting a director should heatmap all their movies.
Inputting an actor should heatmpa all of their movies.
Any more interesting data that can be extracted and mapped is welcome!

🚦 Running the Project

Clone the repository
Get yourself an API key here: https://imdbapi.dev/
Put your API into the python script
Go to IMDB and find the names of the show and its IMDB ID (found in the url for that shows imdb page)
Either make a list and pass it to the main function or run the main function and manually put your show and id in.
