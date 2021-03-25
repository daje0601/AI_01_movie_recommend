from flask import Flask, render_template, request
import requests
import json


app = Flask("moive")

@app.route("/")
def home():
    movie_api = "https://yts.mx/api/v2/list_movies.json?sort_by=rating"
    raw_data = requests.get(movie_api)
    parsed_data = json.loads(raw_data.text)

    movie_lists = parsed_data["data"]["movies"]

    title_list = []
    
    for m_list in movie_lists:
        title_list.append(m_list["title"])

    return render_template("index.html", title=title_list, testtest=movie_lists), 200 


@app.route("/movie")
def movie_page():

    return "Hello, Welcome to"


if __name__ == "__main__":

    app.run(debug=True)
