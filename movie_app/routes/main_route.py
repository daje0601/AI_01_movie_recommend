from flask import Blueprint, render_template, request, redirect, url_for
from movie_app.utils import main_funcs
from flask import Flask, render_template, request
import requests
import json
from movie_app import db
from movie_app.models import movie_model

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/compare", methods=["GET", "POST"])
def compare_index():

    prediction = None

    if request.method == "POST":
        text_to_compare = request.form["compare_text"]

        prediction = {
            "result": main_funcs.predict_text(text_to_compare),
            "compare_text": text_to_compare,
        }
        return render_template("recommend_movie.html", prediction=prediction)
    return render_template("recommend_movie.html"), 200


@bp.route("/movie", methods=["GET", "POST"])
def moive_index():
    """
    user_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
    """
    movie_api = "https://yts.mx/api/v2/list_movies.json?sort_by=rating"
    raw_data = requests.get(movie_api)
    parsed_data = json.loads(raw_data.text)

    movie = parsed_data["data"]["movies"]

    if request.method == "POST":
        likeit = request.form["toupload"]
        upload_to_likelist = movie_model.Likelist(moviename=likeit)
        db.session.add(upload_to_likelist)
        db.session.commit()

    return render_template("moive.html", movie=movie)


@bp.route("/login")
def login_index():
    return render_template("login.html")


@bp.route("/likeitlist", methods=["GET"])
def likeitlist_index():

    display_likelist = movie_model.Likelist.query.all()

    if request.method == "POST":
        likeit = request.form["toupload"]
        upload_to_likelist = movie_model.Likelist(moviename=likeit)
        db.session.add(upload_to_likelist)
        db.session.commit()

    return render_template("likeitlist.html", display_likelist=display_likelist)


@bp.route("/likeitlist", methods=["GET"])
def delete_likeitlist_index():
    delete_moviename = request.form["delete_movie"]

    moviename = movie_model.Likelist.query.filter(
        movie_model.Likelist.moviename == delete_moviename
    ).first()
    db.session.delete(moviename)
    db.session.commit()

    return render_template("likeitlist.html")