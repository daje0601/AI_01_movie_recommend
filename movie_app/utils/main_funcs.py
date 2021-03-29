from movie_app.services.embedding_api import en
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import requests
import json


def msg_processor(msg_code):
    """
    msg_processor returns a msg object with 'msg', 'type'
    where 'msg' corresponds to the message user sees
    and 'type' is the color of the alert element

    codes:
        - 0 : Successfully added to database
        - 1 : User does not exist
        - 2 : Unable to retrieve tweets
        - 3 : Successfully deleted user
    """

    msg_code = int(msg_code)

    msg_list = [
        ("Successfully added to database", "success"),
        ("User does not exist", "warning"),
        ("Unable to retrieve tweets", "warning"),
        ("Successfully deleted user", "info"),
    ]

    return {"msg": msg_list[msg_code][0], "type": msg_list[msg_code][1]}


def predict_text(predict_text):
    movie_api = "https://yts.mx/api/v2/list_movies.json?sort_by=rating"
    raw_data = requests.get(movie_api)
    parsed_data = json.loads(raw_data.text)

    movie = parsed_data["data"]["movies"]

    X = []
    y = []
    for mv in movie:
        X.append(mv["summary"])
        y.append(mv["title"])

    vecs = en.encode(texts=X)
    vecs = en.encode(texts=y)

    classifier = RandomForestClassifier()
    classifier.fit(vecs, y)

    predict_embedding = en.encode(texts=[predict_text])
    prediction = classifier.predict(predict_embedding)

    print(f"Prediction Results {prediction[0]}")

    return prediction[0]
